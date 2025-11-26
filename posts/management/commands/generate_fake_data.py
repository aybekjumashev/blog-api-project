import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker
from posts.models import Post, Category, Tag, Comment

class Command(BaseCommand):
    help = 'Test ushın feyk maǵlıwmatlar jaratıw'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Sanlar (Siz soraganday)
        USERS_COUNT = 1000
        CATEGORIES_COUNT = 50
        POSTS_COUNT = 2000
        TAGS_COUNT = 300
        COMMENTS_COUNT = 3000

        self.stdout.write("Maǵlıwmatlar jaratılıwı baslandı...")

        # Tranzakciya qollanıw (eger qáte shıqsa, barlıǵın biykar qılıw ushın)
        with transaction.atomic():
            
            # 1. USERLERDI JARATIW
            self.stdout.write(f"{USERS_COUNT} user jaratılıp atır...")
            users = []
            for _ in range(USERS_COUNT):
                username = fake.unique.user_name()
                # Userler tez jaratılıwı ushın modeldi tuwrıdan-tuwrı shaqıramız
                users.append(User(
                    username=username,
                    email=fake.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                ))
            # bulk_create tez isleydu
            User.objects.bulk_create(users)
            # ID-lardı alıw ushın bazadan qayta oqıymız
            all_users = list(User.objects.all())

            # 2. KATEGORIYALARDI JARATIW
            self.stdout.write(f"{CATEGORIES_COUNT} kategoriya jaratılıp atır...")
            categories = []
            for _ in range(CATEGORIES_COUNT):
                # Tiykarǵı sóz qaytalanbaslıǵı ushın 'uuid4' yamasa qosımsha san qosıw múmkin
                # Biraq faker.unique kóbirek waqıt alıwı múmkin, sońlıqtan ápiwayı jol:
                name = f"{fake.word()} {random.randint(1, 10000)}"
                categories.append(Category(name=name))
            Category.objects.bulk_create(categories, ignore_conflicts=True)
            all_categories = list(Category.objects.all())

            # 3. POSTLARDI JARATIW
            self.stdout.write(f"{POSTS_COUNT} post jaratılıp atır...")
            posts = []
            for _ in range(POSTS_COUNT):
                posts.append(Post(
                    author=random.choice(all_users),
                    title=fake.sentence(),
                    content=fake.text(max_nb_chars=1000),
                    category=random.choice(all_categories) if all_categories else None
                ))
            Post.objects.bulk_create(posts)
            all_posts = list(Post.objects.all())

            # 4. TAGLARDI JARATIW
            self.stdout.write(f"{TAGS_COUNT} tag jaratılıp atır...")
            tags = []
            for _ in range(TAGS_COUNT):
                name = f"{fake.word()}_{random.randint(1, 10000)}"
                tags.append(Tag(name=name))
            Tag.objects.bulk_create(tags, ignore_conflicts=True)
            all_tags = list(Tag.objects.all())

            # Postlarǵa Taglardı baylanıstırıw (ManyToMany)
            self.stdout.write("Taglar postlarǵa baylanıstırılıp atır...")
            # Hár bir tag ushın 5-10 random post tańlap alamız
            for tag in all_tags:
                random_posts = random.sample(all_posts, k=random.randint(5, 20))
                # Modelde Tag.posts bar bolǵanı ushın:
                tag.posts.set(random_posts)

            # 5. KOMMENTARIYALARDI JARATIW
            self.stdout.write(f"{COMMENTS_COUNT} kommentariya jaratılıp atır...")
            comments = []
            for _ in range(COMMENTS_COUNT):
                comments.append(Comment(
                    post=random.choice(all_posts),
                    author=random.choice(all_users),
                    content=fake.sentence()
                ))
            Comment.objects.bulk_create(comments)

        self.stdout.write(self.style.SUCCESS(f"JUWMAQLANDI! Barlıq maǵlıwmatlar bazada."))