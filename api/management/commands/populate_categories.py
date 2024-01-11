from django.apps import apps
from django.core.management.base import BaseCommand



from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populates the database with categories.'

    def handle(self, *args, **options):
        print('Populating the database...')

        Category = apps.get_model('api', 'Category')
        
        category_names = [
            'AUTOMOTIVE', 'BABY CARE', 'BEAUTY', 'BEVERAGES', 'BOOKS',
            'BREAD/BAKERY', 'CELEBRATION', 'CLEANING', 'DAIRY', 'DELI', 'EGGS',
            'FROZEN FOODS', 'GROCERY I', 'GROCERY II', 'HARDWARE',
            'HOME AND KITCHEN I', 'HOME AND KITCHEN II', 'HOME APPLIANCES',
            'HOME CARE', 'LADIESWEAR', 'LAWN AND GARDEN', 'LINGERIE',
            'LIQUOR,WINE,BEER', 'MAGAZINES', 'MEATS', 'PERSONAL CARE',
            'PET SUPPLIES', 'PLAYERS AND ELECTRONICS', 'POULTRY',
            'PREPARED FOODS', 'PRODUCE', 'SCHOOL AND OFFICE SUPPLIES',
            'SEAFOOD'
        ]

        categories= []
        for category_name in category_names:
            categories.append(Category(name=category_name))
        
        Category.objects.bulk_create(categories)


        self.stdout.write(self.style.SUCCESS("Successfully populated db with categories..."))