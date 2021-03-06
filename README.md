# printbar_to_pinterest
Extracts products from printbar.ru and upload to pinterest.com.
# how it works
Products name, price, image and url extract from printbar.ru and immediately uploaded to pinterest.ru
Data transfer principle table:
| printbar product page| pinterest pin |
| ------------- |:-------------:| 
| name | name|
| image | image |
| price | description|
| url | target link|

Example:
| printbar product page| pinterest pin |
| :-------------:|:-------------:| 
| Мужская футболка DAB панда дед мороз | Мужская футболка DAB панда дед мороз |
| image.jpg | image.jpg |
| 1099 ₽| Цена: 1099 ₽. Принт выдерживает неограниченное количество стирок. Выберите тип ткани и вид печати. Продукция будет готова через 48 часов. #Мужская #футболка #Воин|
| https://printbar.ru/muzhskiye-futbolki/futbolka-dab-panda-ded-moroz-1866669/ | https://{alias}/muzhskiye-futbolki/futbolka-dab-panda-ded-moroz-1866669/|

Hashtags generated automatically and consists from product name, where spaces replaced by #. 

For example: product name 'Мужская футболка Boom' will change to '#Мужская #футболка #Boom'.
{alias} is a your shop url. See below.
# configuration
## config/account.json
Set your pinterest profile information. cred_root dir automatically created.
```
{
    "email":"your_email",
    "password":"your_password",
    "username":"pinterest_username",
    "cred_root":"cookies_dir",
    "user_agent": "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0"
}
```
## config/board_data.json
```
{
    "pinterest_board_name": "printbar_catalog_url",
    "games": "https://printbar.ru/muzhskiye-tovari/igry/"
}
```
If pinterest board doesn't exist, it will be created.
## config/settings.json
```
{
    "alias": "your_printbar_shop_url",
    "pin_creating_period": 25,
    "board_creating_period": 500
}
```
 pin_creating_period and board_creating_period measured in seconds

'alias' is replacing on 'printbar.ru' in product url. alias = 'bestmerch.printbar.ru'
Example:
```
product url 'https://printbar.ru/muzhskiye-futbolki/futbolki-vlad-a4-2818453/' -> pin url 'https://bestmerch.printbar.ru/muzhskiye-futbolki/futbolki-vlad-a4-2818453/'
```
# requirements
```
pip3 install py3-pinterest beautifulsoup4 requests lxml
```
or use .venv
# how to run
```
./run
```
