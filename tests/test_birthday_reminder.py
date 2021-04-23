# -*- coding: utf-8 -*-
from odoo.tests import common


class TestBirthdayReminder(common.TransactionCase):
    def test_create_data(self):
        test_department = self.env['hr.department'].create({
            'name': 'Test Department',
            'remind_before': 5
        })

        test_employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'birthday': '1987-04-07',
            'department_id': test_department.id,
            'include_in_birthday_reminder_list': True
        })

        employee = None
        for i in test_department.birthday_reminder_list:
            if i.id == test_employee.id:
                employee = i

        self.assertEqual(test_department.id, test_employee.department_id.id)
        self.assertEqual(test_department.name, test_employee.department_id.name)
        self.assertEqual(test_employee.id, employee.id)
        print('test ran successfully')