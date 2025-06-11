import phonenumbers
from phonenumbers import geocoder
phone_number1 = phonenumbers.parse("+917435991877")
phone_number2 = phonenumbers.parse("+918238622366")

print(geocoder.description_for_number(phone_number1,"en"))
print(geocoder.description_for_number(phone_number2,"en"))

