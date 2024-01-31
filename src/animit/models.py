from django.db import models
from django.contrib.auth.models import AbstractUser

# デフォルトのanimal_id
DEFAULT_ANIMAL_ID = 1

class Animal(models.Model):
    animal_name = models.CharField(max_length=100)
    sentence_ender = models.CharField(max_length=15)
    # animal_icon = models.ImageField
    
    
    def __str__(self) -> str:
        return self.animal_name
    
class AnimitUser(AbstractUser):
    # _() 関数は、文字列をマークして、それが翻訳対象であることを示す
    email = models.EmailField(max_length=254, blank=False, unique=True)
    username = models.CharField(max_length=15, unique=True, blank=False)
    userid = models.CharField(max_length=15, unique=True, blank=False)
   
    
    animal_id = models.ForeignKey(Animal, 
                                  related_name="animit_users",     #  親データから子データ一覧を逆参照する際はanimit_usersという名前で参照できる
                                  to_field='id',                   # AnimalUserモデルはAnimalモデルのidフィールドを外部参照する
                                  on_delete=models.SET_DEFAULT,   # 外部参照しているanimalオブジェクトが削除されたときはデフォルト値をセットする
                                  default=DEFAULT_ANIMAL_ID)       # デフォルト値はDEFAULT_ANIMAL_IDとする
    
    # 使用しないフィールドを非活性化
    first_name = models.CharField(('first name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return str(self.id)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="animituser_groups",  # Related name changed to avoid conflict
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="animituser_permissions",  # Related name changed to avoid conflict
        related_query_name="user",
    )
    
