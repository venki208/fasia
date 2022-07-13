from app import app
from flask_mandrill import Mandrill

mandrill = Mandrill(app)

class MandrillMail:

	@classmethod
	def send_mail(self, template_name, email_to, reply_to=None, context={}):
		to =[{'email': email} for email in email_to]
		context_dict = [{'name':k, 'content': v} for k, v in context.items()]
		mail_response = mandrill.send_email(
		    to=to,
		    template_name = template_name,
		    headers = { "Reply-To": reply_to } if reply_to  else {},
		    global_merge_vars = context_dict,
		)
		return mail_response