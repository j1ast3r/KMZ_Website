from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from django.contrib.auth.models import User
from django.utils.dateparse import parse_time
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Seat(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='seats')
    row = models.IntegerField()
    number = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_reserved = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'row', 'number')

    def __str__(self):
        return f"Event: {self.event.name}, Row: {self.row}, Seat: {self.number}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.event.price
        super().save(*args, **kwargs)


def save(self, *args, **kwargs):
    if self.image:
        img = Image.open(self.image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        output_size = (300, 200)
        img.thumbnail(output_size)
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        self.image = ContentFile(output.read(), name=f"{self.name}.jpg")
    super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='tickets')
    is_reserved = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket for {self.event.name} - {self.seat}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat} in cart for {self.cart.user.username}"


@receiver(post_save, sender=Event)
def create_seats(sender, instance, created, **kwargs):
    if created:
        row_seats = {
            1: 8, 2: 16, 3: 16, 4: 16, 5: 16, 6: 16,
            7: 18, 8: 18, 9: 18, 10: 18, 11: 18, 12: 18, 13: 18, 14: 18,
            15: 22, 16: 22, 17: 22, 18: 22, 19: 22, 20: 22, 21: 22, 22: 22, 23: 22,
            24: 26, 25: 26, 26: 22, 27: 18, 28: 14, 29: 12, 30: 14, 31: 26, 32: 24, 33: 18
        }

        for row, seats in row_seats.items():
            for seat_number in range(1, seats + 1):
                Seat.objects.create(
                    event=instance,
                    row=row,
                    number=seat_number,
                    price=instance.price  # Используем цену события
                )