HTML_EMAIL_BODY_TEMPLATE = """
<html>
  <body>
    <p>Здравствуйте, {name}!</p>
    <p>Мы получили запрос на сброс пароля для вашей учетной записи.  
       Для завершения процесса нажмите на кнопку ниже (действует в течение <strong>{duration} часа</strong>):</p>
    
    <a href="http://{url}/reset-password?token={token}" 
       style="display: inline-block; padding: 12px 24px; background: #007BFF; 
              color: white; text-decoration: none; border-radius: 4px;">
       Сбросить пароль
    </a>

    <p>Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.</p>
    <p><strong>Важно:</strong> Ссылка одноразовая и станет недействительной после истечения срока или использования.</p>
    
    <p>С уважением,<br>
       Команда IT школа<br>
       <a href="mailto:support@example.com">support@example.com</a></p>
  </body>
</html>
"""

HTML_EMAIL_SUBJECT_TEMPLATE = """
IT школа. Сброс пароля
"""