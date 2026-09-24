راهنمای اجرای پروژه سیستم مهارت‌جویی  
=
در این راهنما مراحل اجرای پروژه سیستم مهارت‌جویی بر روی سیستم شما توضیح داده شده است.  
  

پیش‌نیازها
-
- نصب Python 3.12.6 یا نسخه‌های بالاتر (در صورت عدم نصب، ابتدا آن را از https://www.python.org دریافت و نصب کنید)
- نصب Git
- اتصال به اینترنت

  
مراحل اجرا
-
1.ساخت پوشه پروژه  
ابتدا CMD را اجرا کرده و پوشه‌ای برای پروژه بسازید:  
<pre>mkdir folderName</pre>
2.کلون کردن ریپازیتوری نهایی  
با Git Bash وارد پوشه شوید و ریپازیتوری Skill-Matching-System را clone کنید:  
<pre>cd folderName 
git clone https://github.com/Negar-Niksirat/Skill-Matching-System.git</pre>
3.ساخت و فعال‌سازی محیط مجازی  
در CMD دستور زیر را اجرا کنید:  
<pre>cd folderName
python -m venv venvName</pre>
فعال‌سازی محیط مجازی:  
<pre>cd venvName\Scripts
activate</pre>
بعد از فعال‌سازی، نام محیط مجازی در ابتدای خط فرمان نمایش داده می‌شود.  
4.نصب فایل requirements.txt  
با محیط مجازی فعال در پوشه cangrow2_final که فایل requirements.txt قرار دارد، دستور زیر را اجرا کنید:  

<pre>pip install -r requirements.txt</pre>
5.تنظیم API Key  
برای اتصال به API هوش مصنوعی، از سایت https://openrouter.ai/settings/keys یک API Key دریافت کنید. سپس در پوشه‌ی پروژه، فایل env. را ایجاد کرده و کلید را وارد نمایید:
<pre>echo API_KEY=yourAPIKey >> .env</pre>

6.اجرای فایل آموزش مدل  
در پوشه cangrow2_final بروید و اسکریپت آموزش مدل را اجرا کنید:  

<pre>python -m source_code.train_model</pre>
7.اجرای رابط کاربری  
برای اجرای رابط گرافیکی برنامه با Streamlit، دستور زیر را وارد کنید:  

<pre>streamlit run app.py</pre>
