#admin
http://127.0.0.1:8000/admin/
#sender
http://127.0.0.1:8000/email_sender/home/


#api
http://127.0.0.1:8000/api/users/register/
http://127.0.0.1:8000/api/users/login/
http://127.0.0.1:8000/api/users/profile/
http://127.0.0.1:8000/api/users/profiles/


api/users/ register/ [name='register']
api/users/ login/ [name='login']
api/users/ profile/ [name='profile']
api/users/ profiles/ [name='profiles']
api/users/ logout/ [name='logout']
api/users/ change_password/ [name='change_password']
api/users/ users/<int:pk>/ [name='user_detail']
api/users/ users/<int:pk>/status/ [name='user_status']
api/users/ users/<int:pk>/delete/ [name='user_delete']




#api schemas
http://127.0.0.1:8000/api/docs/
http://127.0.0.1:8000/api/schema/      yaml-файл