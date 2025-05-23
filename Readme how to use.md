راهنمای اجرای پروژه سیستم مهارت‌جویی  
=
در این راهنما مراحل اجرای پروژه سیستم مهارت‌جویی بر روی سیستم شما توضیح داده شده است.  
**نکته مهم:** اگر فایل `README how to use.md` موجود در ریپازیتوری [`NegarNiksirat_cangrow2_raw`](https://github.com/Negar-Niksirat/NegarNiksirat_cangrow2_raw) را مطالعه نکرده‌اید، ابتدا آن را بخوانید و مراحل اولیه نصب را انجام دهید. سپس ادامه‌ی این راهنما را دنبال کنید.  

مراحل اجرا
-
1.کلون کردن ریپازیتوری نهایی  
با Git Bash وارد پوشه‌ی ساخته شده شوید و ریپازیتوری cangrow2_final را clone کنید:  
<pre>cd folderName 
git clone https://github.com/Negar-Niksirat/cangrow2_final.git</pre>
2.فعال‌سازی محیط مجازی:  
وارد مسیر اسکریپت‌های محیط مجازی شوید و آن را فعال کنید:  
<pre>cd venvName\Scripts
 activate</pre>
بعد از فعال‌سازی، نام محیط مجازی در ابتدای خط فرمان نمایش داده می‌شود.  
3. اجرای فایل آموزش مدل  
به پوشه cangrow2_final بروید و اسکریپت آموزش مدل را اجرا کنید:  

<pre>python -m source_code.train_model</pre>
4. اجرای رابط کاربری
برای اجرای رابط گرافیکی برنامه با Streamlit، دستور زیر را وارد کنید:  

<pre>streamlit run app.py</pre>
