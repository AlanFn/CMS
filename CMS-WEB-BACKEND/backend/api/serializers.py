from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Libro, Categoria, UserProfile


#para el manejo de los jsons
class LibroSerializer(serializers.ModelSerializer):
    categoriaNombre = serializers.CharField(source='categoria.nombre', read_only=True)
    autorNombre = serializers.CharField(source='author.username', read_only=True)

    """Serilizer para un articulo con los atributos id, titulo, fecha, autor, categoria"""
    class Meta:
        model = Libro
        fields = ["id", "titulo", "fecha", "author", "categoria", "contenido", "likes", "vistas", "categoriaNombre", "autorNombre"]
        extra_kwargs ={"autor": {"read_only": True}}


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para una categoria con atributos id y nombre"""
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]



class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='userprofile.role', read_only=True)

    """Serializer para un usuario con atributos id, username y password
    """
    class Meta:
        model = User
        fields = ["id", "username", "password", "role"]
        extra_kwargs = {"password": {"write_only":True}}
    
    #para el registro una vez se convierte al modelo user validate_data ya comprueba si esta todo correcto en la clase userSerializer
    def create (self, validated_data):
        """Método reescrito, se crea el usuario una vez que el objeto validated_data sea correcto"""
        user = User.objects.create_user(**validated_data)
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    
    """
    serializer para el perfil de cada usuario.-
    """
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ["user","rol"]
  
  
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
        Utilizamos un serializer diferente para el update, para que solo podamos
        editar el role del userprofile, sin pasarle el user.-
    """    
     
    class Meta:
        model = UserProfile
        fields = ['role']  # Solo permitimos actualizar el campo 'role'
