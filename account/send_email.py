from django.core.mail import send_mail
from django.utils.html import format_html
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_confirmation_email(email , code):
    activation_url = f'http://127.0.0.1:8000/api/account/activate/?u={code}'
    context = {'activation_url': activation_url}
    subject = 'Здраствуйте потвердите свое присудствие '
    html_message = render_to_string('activate.html',context)
    plain_message = strip_tags(html_message)
    
    
    send_mail(
        subject,
        plain_message,
        'ITInternHub@gmail.com',
        [email],
        html_message=html_message,
        fail_silently=False
    )
    
def send_confirmation_password(email,code):
    
    send_mail(
            'Подтвердите ваше изменение',
            f'Ваш код подтверждение: {code}',
            'ITInternHub@gmail.com',
            [email],
            fail_silently=False,
        )
    


def send_respond_data(full_name, characteristics, phone_number, email, short_intro, additional_info, owner_email):
    subject = 'New Job Application'
    message = f'You have a new job application:\n\nFull Name: {full_name}\nCharacteristics: {characteristics}\nPhone Number: {phone_number}\nEmail: {email}\nShort Intro: {short_intro}\nAdditional Info: {additional_info}'
    from_email = 'your_email@example.com'
    recipient_list = [owner_email]

    send_mail(subject, message, from_email, recipient_list)




from post.models import Post
def send_comment_notification(post_author,content,email_from):
    post_user = Post.objects.get(pk=post_author)
    subject = 'New Comment on Your Post'
    message = f'Hello {post_user.author.first_name},\n\n' \
              f'There is a new comment on your post "{post_user.title}".\n\n' \
              f'Comment: {content}\n\n' \
              f'Visit the post: {email_from}'
    from_email = f'{email_from}'
    recipient_list = [post_user.author.email]

    send_mail(subject, message, from_email, recipient_list)
