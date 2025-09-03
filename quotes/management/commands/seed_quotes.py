from django.core.management.base import BaseCommand
from quotes.models import Source, Quote


DATA = {
    ("Матрица", "фильм"): [
        ("Ложки не существует.", 3),
        ("К сожалению, невозможно объяснить, что такое Матрица.", 2),
        ("Я знаю кунг-фу.", 1),
    ],
    ("Дюна", "книга"): [
        ("Страх убивает разум.", 4),
        ("Специя должна течь.", 2),
    ],
}


class Command(BaseCommand):
    help = "Загрузка демо-данных (источники и цитаты). Повторный запуск безопасен."

    def handle(self, *args, **options):
        created_sources = 0
        created_quotes = 0

        for (name, typ), quotes in DATA.items():
            src, src_created = Source.objects.get_or_create(name=name, defaults={"type": typ})
            if src_created:
                created_sources += 1
            elif src.type != typ:
                src.type = typ
                src.save(update_fields=["type"])

            for text, weight in quotes:
                obj, q_created = Quote.objects.get_or_create(
                    text=text,
                    defaults={"source": src, "weight": weight},
                )
                if q_created:
                    created_quotes += 1
                else:
                    changed = False
                    if obj.source_id != src.id:
                        obj.source = src
                        changed = True
                    if obj.weight != weight:
                        obj.weight = weight
                        changed = True
                    if changed:
                        obj.save(update_fields=["source", "weight"])

        self.stdout.write(self.style.SUCCESS(
            f"Импорт завершён. Источников: {created_sources}, цитат: {created_quotes}"
        ))
