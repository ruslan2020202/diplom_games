import flask_marshmallow as ma


class Schema(ma.Schema):
    class Meta:
        fields = ('name', 'total_point')


user_schema = Schema(many=True)
