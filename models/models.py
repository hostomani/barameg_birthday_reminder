# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    remind_before = fields.Integer()
    birthday_reminder_list = fields.Many2many('hr.employee')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    include_in_birthday_reminder_list = fields.Boolean()
    next_birthday = fields.Date(compute='_next_birthday', search='_search_next_birthday')
    birthday_remind_date = fields.Date(compute='_birthday_remind_date', search='_search_remind_date')

    def _search_next_birthday(self, operator, value):
        employees = self.search([])
        if employees:
            list = []
            for employee in employees:
                if value == str(employee._next_birthday()).split(' ')[0]:
                    list.append(employee.id)
            return [('id', 'in', list)]

    def _search_remind_date(self, operator, value):
        employees = self.search([])
        if employees:
            list = []
            for employee in employees:
                if value == str(employee._birthday_remind_date()).split(' ')[0]:
                    list.append(employee.id)
            return [('id', 'in', list)]

    @api.model
    def create(self, values):
        rec = super(HrEmployee, self).create(values)
        try:
            if rec.include_in_birthday_reminder_list:
                if rec.department_id and rec.birthday:
                    reminders_list = []
                    for i in rec.department_id.birthday_reminder_list:
                        reminders_list.append(i.id)
                    reminders_list.append(rec.id)
                    self.department_id.write({'birthday_reminder_list': [[6, 0, reminders_list]]})
                else:
                    raise exceptions.ValidationError('Department and birthday are required')
        except Exception as e:
            raise exceptions.UserError(e)
        else:
            return rec

    def write(self, values):
        rec = super(HrEmployee, self).write(values)
        if 'include_in_birthday_reminder_list' in values:
            if values['include_in_birthday_reminder_list']:
                if self.department_id and self.birthday:
                    reminders_list = []
                    for i in self.department_id.birthday_reminder_list:
                        reminders_list.append(i.id)
                    reminders_list.append(self.id)
                    self.department_id.write({'birthday_reminder_list': [[6, 0, reminders_list]]})
            else:
                if self.department_id:
                    reminders_list = []
                    for i in self.department_id.birthday_reminder_list:
                        if i.id != self.id:
                            reminders_list.append(i.id)
                    self.department_id.write({'birthday_reminder_list': [[6, 0, reminders_list]]})
        else:
            return super(HrEmployee, self).write(values)

    @api.depends('birthday')
    def _next_birthday(self):
        today = datetime.date(datetime.now())
        for rec in self:
            if rec.birthday:
                if today.month == rec.birthday.month:
                    if today.day < rec.birthday.day:
                        year = str(today.year)
                        month = str(rec.birthday.month)
                        while len(month) < 2: month = '0' + month
                        day = str(rec.birthday.day)
                        while len(day) < 2: day = '0' + day
                        date_str = year + '-' + month + '-' + day
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        rec.next_birthday = date
                        return date
                    else:
                        year = str(today.year + 1)
                        month = str(rec.birthday.month)
                        while len(month) < 2: month = '0' + month
                        day = str(rec.birthday.day)
                        while len(day) < 2: day = '0' + day
                        date_str = year + '-' + month + '-' + day
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        rec.next_birthday = date
                        return date
                if today.month > rec.birthday.month:
                    year = str(today.year + 1)
                    month = str(rec.birthday.month)
                    while len(month) < 2: month = '0' + month
                    day = str(rec.birthday.day)
                    while len(day) < 2: day = '0' + day
                    date_str = year + '-' + month + '-' + day
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    rec.next_birthday = date
                    return date
                if today.month < rec.birthday.month:
                    year = str(today.year)
                    month = str(rec.birthday.month)
                    while len(month) < 2: month = '0' + month
                    day = str(rec.birthday.day)
                    while len(day) < 2: day = '0' + day
                    date_str = year + '-' + month + '-' + day
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    rec.next_birthday = date
                    return date
            else:
                rec.next_birthday = False
                rec.include_in_birthday_reminder_list = False
                return False

    @api.depends('birthday','next_birthday' )
    def _birthday_remind_date(self):
        if self.birthday:
            remind_before = self.department_id.remind_before
            date = self.next_birthday - timedelta(days=remind_before)
            self.birthday_remind_date = date
            return date
        else:
            self.birthday_remind_date = False
            return False

    def send_birthday_reminder(self):
        departments = self.env['hr.department'].search([])
        for department in departments:
            employees = department.birthday_reminder_list
            for employee in employees:
                template = self.env.ref('barameg_birthday_reminder.birthday_reminder')
                self.env['mail.template'].browse(template.id).send_mail(employee.id)
