from sql_alchemy import banco


# banco.model é para incluir o banco
class SiteModel(banco.Model):
    __tablename__ = 'sites'
    # colunas da tabela
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')# lista de objetos hoteis


    def __init__(self, url):
        self.url = url


    # converte em json os atributos
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'url': self.url,
            'hoteis':[hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()

