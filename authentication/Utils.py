import templated_mail.mail


def activation_email(to, context):
    return templated_mail.mail.BaseEmailMessage(context=context, template_name='email/activation.html').send(to=[to])


def password_reset_email(to, context):
    return templated_mail.mail.BaseEmailMessage(context=context, template_name='email/password-reset.html').send(to=[to])
