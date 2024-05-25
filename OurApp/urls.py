from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('sign-up/',views.SignUpView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('room/',views.RoomView.as_view()),
    path('recommandDoctor/',views.RecommandDoctor),
    path('demmandRendezVous/',views.DemmandRendezVous),
    path('listDesRendezVous/',views.ListDesRendezVous),
    path('rpndrRendezVous/',views.RpndrRendezVous),
    path('demandeAllRapport/',views.demandeAllRapport),
    path('getDemmandAllRapport/',views.GetDemmandAllRapport),
    path('rpndrADemmandeAllRapport/',views.rpndrADemmandeAllRapport),
    path('getAllRapportByMedecin/',views.GetAllRapportByMedecin),
    path('sendMsg/',views.SendMsg)
]


