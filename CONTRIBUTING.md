# Coding Rules

## Folder Structure

api/
models/
schemas/
services/
repositories/

---

## One owner per module.

Vehicle -> Member 2

Driver -> Member 3

Trip -> Khubi

---

## Never modify another person's module.

---

## Don't change API responses.

---

## Follow Trip module style.

---

## Every model must

- inherit Base
- inherit BaseModel
- use Mapped
- use mapped_column
- use __repr__