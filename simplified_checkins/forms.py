from django import forms


class CheckCheckinsForm(forms.Form):
    hostname = forms.CharField(
        label="hostname",
        initial="http://localhost",
    )
    port = forms.CharField(
        label="port",
        initial="9990",
    )
    path = forms.CharField(
        label="path",
        initial="/all",
    )
