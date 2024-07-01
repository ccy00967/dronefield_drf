from rest_framework import serializers;
from customer.models import CustomerRequest;

class CustomerRequestSerializer(serializers.ModelSerializer):
    # 외래키인 owner.[내용물]로 값을 리턴받을 수 있다, 물론 아래 Meta클래스의 필드에도 추가해야한다
    ownerEmail = serializers.ReadOnlyField(source='owner.email')
    ownerName = serializers.ReadOnlyField(source='owner.name')


    class Meta:
        model=CustomerRequest
        fields= (
            'id',
            'ownerEmail',
            'ownerName',
            'address',
            'requestContent',
            'reservationDate',
        )
        # fields = '__all__'


