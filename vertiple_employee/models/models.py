# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
from odoo.exceptions import ValidationError
from odoo import exceptions, _

class vertiple_employee(models.Model):
	#_name = 'vertiple_employee.vertiple_employee'
	_inherit = 'hr.employee'

	employee_id = fields.Char(string='Employee ID', readonly=True)
	#emp_name  	= fields.Char(compute='get_emp_name',string="Name")
	first_name = fields.Char(string="First Name")
	last_name = fields.Char(string="Last Name")
	fathers_name = fields.Char("Father's Name")
	mothers_name = fields.Char("Mother's Name")
	spouse_name = fields.Char('Spouse Name')
	blood_group = fields.Many2one('vertiple_employee.blood_group', string='Blood Group')
	contact_number = fields.Char('Contact Number')
	emergency_contact = fields.Char('Emergency Contact')
	birthday_as_per_cert = fields.Date('Date of Birth (as per certificate)')
	# Fields for Actions on Employee Page
	manager_status = fields.Char('Manager Status', readonly=True)
	manager_feedback = fields.Selection([
        ('good', 'GOOD'),
        ('avg','AVERAGE'),
        ('poor','POOR'),
        ], string='Feedback', default=False)
	hr_status = fields.Char('HR Status', readonly=True)
	hr_feedback = fields.Selection([
         ('good', 'GOOD'),
        ('avg','AVERAGE'),
        ('poor','POOR'),
        ], string='Feedback', default=False)
	probation_date_end = fields.Date('Probation Date End')
	state = fields.Selection([
        ('probation', 'PROBATION'),
        ('manager_review','MANAGER REVIEW'),
        ('hr_review','HR REVIEW'),
        ('confirmed', 'CONFIRMED'),
        ('notice', 'NOTICE / RESIGN'),
        ('exit','EXIT'),
        ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='probation',)
	check_field = fields.Boolean(string="Check", compute='get_user')
	working_address = fields.Char('Working Address', compute='get_working',readonly=True)
	pf_acc_number = fields.Char('PF Account Number')
	emp_id = fields.Char('Employee ID')
	count = fields.Integer(compute='get_seq_value')

	def get_seq_value(self):
		emp_id_obj = self.env['vertiple_employee.employee_id'].search([])
		temp=''
		for rec in emp_id_obj:
			temp = int(rec.starting_num)
		print temp
		self.write({'count':temp})
		return temp



	def generate_emp(self,start):
		check_val = self.env['ir.values'].sudo().get_default('vertiple_employee.employee_config', 'is_active')
		print check_val
		print "newwwwww"

		obj = self.id
		emp_list=[]
		print self.name,"****************"
		emp_id_obj = self.env['vertiple_employee.employee_id'].search([])

		suffix =''
		prefix =''
		prefix_string = ''
		suffix_string = ''
		main_sequence = ''
		len_prefix = ''
		len_suffix = ''
		separator = ''
		length_seq = ''
		length_rand = ''
		starting_num  = ''
		if check_val==True:
			for rec in emp_id_obj:
				suffix = str(rec.suffix)
				prefix = str(rec.prefix)
				prefix_string = str(rec.prefix_string)
				suffix_string = str(rec.suffix_string)
				main_sequence = str(rec.main_sequence)
				len_prefix = str(rec.len_prefix)
				len_suffix = str(rec.len_suffix)
				separator = str(rec.separator)
				length_seq = str(rec.length_seq)
				length_rand = str(rec.length_rand)
				starting_num = str(rec.starting_num)
			

			if prefix == 'empname':
				first =self.first_name
				last =self.last_name
				res = first[:1].upper() + last[:1].upper() 
				print res	
				pre_string = str(res)

			elif prefix == 'company':
				print self.company_id.name
				company = self.company_id.name
				pre_string = str(''.join(word[0] for word in company.split()).upper())

			elif prefix =='custom':
				pre_string = prefix_string
				

			if suffix == 'empname':
				first = self.first_name
				last =self.last_name
				res = first[:1].upper() + last[:1].upper() 
				print res	
				suf_string = str(res)

			elif suffix == 'company':
				print self.company_id.name
				company =self.company_id.name
				suf_string = str(''.join(word[0] for word in company.split()).upper())

			elif suffix =='custom':
				suf_string = suffix_string
							
			if main_sequence == 'seq':
				k = self.get_seq_value()
				print type(k)
				if int(starting_num) == k:
					seq_string = emp_id_obj.get_seq_num(length_seq, int(starting_num)+1)
				else:
					seq_string = emp_id_obj.get_seq_num(length_seq,int(starting_num))


			elif main_sequence == 'rand':
				seq_string = str(''.join(random.choice('0123456789') for i in range(int(length_rand))))
			
			res =  [str(pre_string),str(seq_string),str(separator),str(suf_string)]			
			
			for i in res:
				if i =='False':
					res.remove('False')
			print "before",res
			if str(separator)in res:
				result = str(pre_string) + str(separator)+ str(seq_string)+str(separator) +str(suf_string)
			else:
				result=''.join(res)
			
			print 'result---->',result
			self.write({'emp_id':result})


	@api.onchange('last_name','first_name')
	def concantenation_of_names(self):
		"""Funtionality of Concantenation of First Name & Last Name"""
		for rec in self:
			if (rec.last_name and rec.first_name) and rec.name == False:
				rec.name= str(self.first_name) + " " + str(self.last_name)

	@api.one
	def get_working(self):
		self.working_address = str(self.address_id.name)+",\n"+str(self.address_id.street)+","+str(self.address_id.city)+",\n"+str(self.address_id.zip)+","+str(self.address_id.state_id.name)+",\n"+str(self.address_id.country_id.name)

	@api.one
	@api.depends('check_field')
	def get_user(self):
		if self.user_id.id == self._uid:
			self.check_field = True
		else:
			self.check_field = False
	@api.multi
	def status_approve_manager(self):
		"""Manager's Employee Approval Status"""
		self.write({'manager_status':'Approved'})
		return self.write({'state': 'hr_review'})
	@api.multi
	def status_refuse_manager(self):
		"""Manager's Employee Refusal Status"""
		self.write({'manager_status':'Refused'})
		return self.write({'state': 'hr_review'})
	@api.multi
	def status_approve_hr(self):
		"""HR's Employee Approval Status"""
		self.write({'hr_status': 'Approved'})
		return self.write({'state': 'confirmed'})
	@api.multi
	def status_refuse_hr(self):
		"""HR's Employee Refusal Status"""
		self.write({'hr_status': 'Refused'})
		return self.write({'state': 'notice'})

	@api.multi
	def manager_approve(self):
		"""Set's the manager's status to Approve & sends email notificaiton"""
		self.status_approve_manager()
		template = self.env.ref('email_status_to_hr_template.email_status_to_hr')
		self.env['mail.template'].browse(template.id).send_mail(self.id)

	@api.multi
	def manager_refuse(self):
		"""Set's the manager's status to Refuse & sends email notificaiton"""
		self.status_refuse_manager()
		template = self.env.ref('email_status_to_hr_template.email_status_to_hr')
		self.env['mail.template'].browse(template.id).send_mail(self.id)
	
	@api.multi
	def hr_approve(self):
		"""Set's the hr's status to Approve & sends email notificaiton"""
		self.write({'hr_status': 'Approved'})
		return self.write({'state': 'confirmed'})
	@api.multi
	def hr_refuse(self):
		"""Set's the hr's status to Refuse & sends email notificaiton"""
		if not self.state == 'notice':
			self.write({'hr_status': 'Refused'})
			return self.write({'state': 'notice'})
		else:
			raise ValidationError("Your are already in  %s" % self.state)
	# Workflow Setting Methods
	@api.multi
	def set_to_probation(self):
		self.write({'state': 'probation'})

	@api.multi
	def set_to_manager_review(self):
		self.write({'state': 'manager_review'})

	@api.multi
	def action_hr_review(self):
		self.write({'state': 'hr_review'})

	@api.multi
	def set_to_confirm(self):
		return self.write({'state': 'confirmed'})

	@api.multi
	def set_to_notice(self):
		self.write({'state': 'notice'})
	@api.multi
	def set_to_exit(self):
		self.write({'state': 'exit'})

	@api.multi
	def emp_resign(self):
		"""Send's email and changes state to notice"""
		if not self.state == 'notice':
			self.sudo().set_to_notice()
		else:
			raise ValidationError("Your are already in  %s" % self.state)
	def change_emp_id(self):
		emp_obj = self.env['vertiple_employee.employee_id'].search([])
		return int(emp_obj.change_emp_id())


class BloodGroup(models.Model):
	_name = 'vertiple_employee.blood_group'
	name = fields.Char(string="Blood Group", required=True,) 

class EmployeeConfig(models.TransientModel):
	_name='vertiple_employee.employee_config'
	_inherit = 'res.config.settings'

	is_active = fields.Boolean(string ="Configure Employee Id")

	# new_field = fields.Boolean(compute='set_is_active')

	@api.multi
	def set_is_active(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_config','is_active',self.is_active)
	# def emp_id_config(self):

	# 	return {
 #            'type': 'ir.actions.act_window',
 #            'name': 'Employee ID',
 #            'view_type': 'form',
 #            'view_mode': 'form',
 #            'res_model': 'vertiple_employee.employee_id',
 #            'res_id': self.env,
 #            'target': 'new',
 #        }
	
	# @api.onchange(active)
	# def enable_config(self):
	# 	if self.active !=True:



#serach for current record ('id','=', self.env.uid)
class Employee_id(models.TransientModel):
	_name='vertiple_employee.employee_id'
	_inherit = 'res.config.settings'

	employee = fields.Many2one('vertiple_employee.vertiple_employee')
	main_sequence = fields.Selection([
        ('seq', 'Sequential'),
        ('rand','Random Number'),
        ], string='Main Sequence', default=None)
	prefix = fields.Selection([
        ('empname', 'Employee F&L Name'),
        ('company','Company Initials'),
        ('custom','Custom'),
        (None,'None'),
        ],string ='Prefix',default=None)
	suffix = fields.Selection([
        ('empname', 'Employee F&L Name'),
        ('company','Company Initials'),
        ('custom','Custom'),
        (None,'None'),
        ],string ='Suffix',default=None)
	prefix_string = fields.Char(string='String')
	suffix_string = fields.Char(string='String')
	len_prefix = fields.Integer(string ='Length')
	len_suffix = fields.Integer(string ='Length')
	separator = fields.Char(string='Separator',default=None)
	length_seq = fields.Integer(string ='Length')
	length_rand = fields.Integer(string ='Length')
	starting_num = fields.Integer(string ='Starting Number')
	count = fields.Integer(default=0)

	@api.multi
	def set_is_active(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','prefix',self.prefix),
	
	@api.multi
	def set_suffix(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','suffix',self.suffix)
	
	@api.multi
	def set_main_sequence(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','main_sequence',self.main_sequence)

	@api.multi
	def set_prefix_string(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','prefix_string',self.prefix_string)

	@api.multi
	def set_suffix_string(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','suffix_string',self.suffix_string)

	@api.multi
	def set_len_prefix(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','len_prefix',self.len_prefix)

	@api.multi
	def set_len_suffix(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','len_suffix',self.len_suffix)

	@api.multi
	def set_seperator(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','separator',self.separator)

	@api.multi
	def set_length_seq(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','length_seq',self.length_seq)

	@api.multi
	def set_length_rand(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','length_rand',self.length_rand)

	@api.multi
	def set_starting_num(self):
		return self.env['ir.values'].sudo().set_default('vertiple_employee.employee_id','starting_num',self.starting_num)

	#@api.onchange('separator')
	def validate_separator(self):
		if len(str(self.separator))>1:
			return True
		else:
			return False

	
	def get_seq_num(self,length,start):
		if start<10:
			temp =str(0)*(int(length)-1)+str(start)
		elif start<100:
			temp =str(0)*(int(length)-2)+str(start)
		elif start<1000:
			temp =str(0)*(int(length)-3)+str(start)
		print temp
		self.count=temp
		return temp


	def get_start_num(self):
		emp_obj = self.env['hr.employee'].search([])
		for rec in emp_obj:
			print rec.count


	def generate_random(self,length):
		return str(''.join(random.choice('0123456789') for i in range(int(self.length_rand))))
	
	# @api.onchange('len_prefix','prefix_string')
	# def validate_prefix(self):
	# 	print "****",self.prefix_string,self.len_prefix
	# 	if self.prefix_string ==False or self.len_prefix==0:
	# 		print "**"
	# 	else:
	# 		if len(str(self.prefix_string))>self.len_prefix:
	# 			raise exceptions.except_orm(_('Error'), _('String Length Exceeded..!!'))

	# @api.onchange('len_suffix','suffix_string')
	# def validate_prefix(self):
	# 	print "****",self.suffix_string,self.len_suffix
	# 	if self.suffix_string ==False or self.len_suffix==0:
	# 		print "**"
	# 	else:
	# 		if len(str(self.suffix_string))>self.len_suffix:
	# 			raise exceptions.except_orm(_('Error'), _('String Length Exceeded.!!'))


	# @api.onchange('separator')
	# def validate_separator(self):
	# 	if self.separator ==False:
	# 		print "@@@@"
	# 	else:
	# 		if len(str(self.separator))>1:
	# 			raise exceptions.except_orm(_('Error'), _('Separator should contain only one charecter ...!!!'))



	# @api.model
	# def create(self,vals):
	# 	if vals['separator'] ==False:
	# 		print "@@@@"
	# 	else:
	# 		if len(str(vals['separator']))>1:
	# 			raise exceptions.except_orm(_('Error'), _('Separator should contain only one charecter ...!!!'))
		
		
	# 	if vals['prefix_string'] ==False or vals['len_prefix']==0:
	# 		print "**"
	# 	else:
	# 		if len(str(vals['prefix_string']))>vals['len_prefix']:
	# 			raise exceptions.except_orm(_('Error'), _('String Length Exceeded..!!'))

	# 	if vals['suffix_string'] ==False or vals['len_suffix']==0:
	# 		print "**"
	# 	else:
	# 		if len(str(vals['suffix_string']))>vals['len_suffix']:
	# 			raise exceptions.except_orm(_('Error'), _('String Length Exceeded.!!'))

	# 	return super(Employee_id, self).create(vals)


	# @api.onchange('prefix','suffix','main_sequence','length_seq','length_rand','starting_num','separator')
	# def change_emp_id(self):
	# 	emp_list=[]
	# 	pre_string =''
	# 	seq_string = ''
	# 	suf_string = ''
	# 	result=''
	# 	temp=0
	# 	start = self.starting_num
	# 	print "*************************"
	# 	obj = self.env['vertiple_employee.employee_id']
	# 	emp_obj = self.env['hr.employee'].search([])
	# 	print emp_obj 
	# 	for rec in emp_obj:
	# 		emp_list.append(rec.emp_id)
	# 	for record in emp_obj:
	# 		if self.prefix == 'empname':
	# 			l = self.env['hr.employee'].browse(record.id)
	# 			first =l.first_name
	# 			last =l.last_name
	# 			res = first[:1].upper() + last[:1].upper() 
	# 			print res	
	# 			pre_string = str(res)

	# 		elif self.prefix == 'company':
	# 			l = self.env['hr.employee'].browse(record.id)
	# 			print l.company_id.name
	# 			company = l.company_id.name
	# 			pre_string = str(''.join(word[0] for word in company.split()).upper())
	# 		elif self.prefix =='custom':
	# 			# if len(str(self.prefix_string)) > self.len_prefix:
	# 			pre_string = self.prefix_string
	# 			# else:
	# 			# 	raise ValidationError('Please check the length of the string')

	# 		if  self.suffix == 'empname':
	# 			l = self.env['hr.employee'].browse(record.id)
	# 			first =l.first_name
	# 			last =l.last_name
	# 			res = first[:1].upper() + last[:1].upper() 
	# 			print res	
	# 			suf_string = str(res)

	# 		elif  self.suffix == 'company':
	# 			l = self.env['hr.employee'].browse(record.id)
	# 			print l.company_id.name
	# 			company = l.company_id.name
	# 			suf_string = str(''.join(word[0] for word in company.split()).upper())

	# 		elif self.suffix =='custom':
	# 			#if len(str(self.suffix_string))>self.len_suffix:
	# 			suf_string = self.suffix_string
	# 			# else:
	# 			# 	raise ValidationError('Please check the length of the string')
				
	# 		if self.main_sequence == 'seq':
	# 			print "cuurent values",self.length_seq, self.starting_num,start
	# 			if start == self.starting_num:
	# 				print "in if"
	# 				seq_string = obj.get_seq_num(self.length_seq, start)
	# 				start+=1
	# 			else:
	# 				seq_string = obj.get_seq_num(self.length_seq, start)
	# 				start+=1

	# 		elif self.main_sequence == 'rand':
	# 			seq_string = str(''.join(random.choice('0123456789') for i in range(int(self.length_rand))))
			
	# 		res =  [str(pre_string),str(seq_string),str(self.separator),str(suf_string)]			
			
	# 		for i in res:
	# 			if i =='False':
	# 				res.remove('False')
	# 		print "before",res
	# 		if str(self.separator)in res:
	# 			result = str(pre_string) + str(self.separator)+ str(seq_string)+str(self.separator) +str(suf_string)
	# 		else:
	# 			result=''.join(res)
			
	# 		print 'result---->',result
	# 		record.write({'emp_id':result})
	# 		print "End of Loop"

	


		
