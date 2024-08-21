from django.core.management.base import BaseCommand
from core.utils.emailThread import EmailThread


class Command(BaseCommand):
    help = 'Send a custom test email using EmailThread'

    def handle(self, *args, **kwargs):
        subject = 'Correo de prueba personalizado'
        email_data = {
            'nombre': 'Juan',
            'mensaje': 'Este es un mensaje personalizado enviado desde un comando de Django.'
        }
        recipient_list = ['updavo@gmail.com']
        template = 'emails/picking_complete.html'

        email_thread = EmailThread(
            subject, email_data, recipient_list, template)

        try:
            email_thread.start()  # Inicia el hilo y envía el correo de manera asíncrona
            self.stdout.write(self.style.SUCCESS(
                'Correo enviado exitosamente en un hilo separado.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error enviando correo: {e}'))
