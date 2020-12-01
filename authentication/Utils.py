from templated_mail.mail import BaseEmailMessage


def activation_email(to, context):
    return BaseEmailMessage(context=context, template_name='email/activation.html').send(to=[to])


def password_reset_email(to, context):
    return BaseEmailMessage(context=context, template_name='email/password-reset.html').send(to=[to])
