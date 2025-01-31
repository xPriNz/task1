Celem niniejszego opracowania jest przeprowadzenie uproszczonego procesu Domain Driven Design (DDD) dla wymyślonego banku. Proces ten pozwoli na lepsze zrozumienie domeny oraz identyfikację kluczowych kontekstów, encji, agregatów i obiektów wartościowych.

W banku można wymienić następujące konteksty:

- Zarządzanie Kontami
- Zarządzanie Przelewami

Encje, agregaty oraz Value Objects:

- Użytkownik
  - Imię i nazwisko
  - PESEL (Value Object)
  - Kontakt
  - Adres
- Dane kontaktowe (Value Object)
  - Nr. telefonu
  - Adres email
- Adres (Value Object)
  - Państwo
  - Miasto
  - Kod pocztowy
  - Ulica
  - Numer budynku
- Konto bankowe
  - Numer rachunku (Value Object)
  - Saldo
  - Użytkownik
- Przelew (wartość)
  - Numer rachunku odbiorcy (Value Object)
  - Numer rachunku nadawcy (Value Object)
  - Kwota (wartość)
  - Data nadania (Value Object)
