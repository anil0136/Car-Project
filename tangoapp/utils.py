from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_view(email, car_name, total_km_driven, total_amount):
    subject = "booking Success fully"
    message = "thank you for booking a car"
    from_email = 'davilkinganil@gmail.com'
    recipeient_list = [email]

    # Use the correct template name with .html extension
    html_message = render_to_string(
        'bill_email_template.html',  # <-- fix here
        {
            'car_name': car_name,
            'total_km_driven': total_km_driven,
            'total_amount': total_amount,
            'current_year': 2025,
        }
    )
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipeient_list,
            html_message=html_message,
            fail_silently=False
        )
        return HttpResponse("Email sent successfully")
    except Exception as e:
        return HttpResponse(f'error sending email :{str(e)}')