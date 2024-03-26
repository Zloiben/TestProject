from fast_api_core.router import Documentation
from .contact_address.router import ContactAddressAPIRouter

v1 = Documentation(
    documentation_path='/v1',
    title='Документация V1',
    version='1.0'
)

contact_address_doc = Documentation('/contact-address', title="Адреса по номеру", version="1.0")
contact_address_doc.include_api_router(ContactAddressAPIRouter())
contact_address_doc.push()

v1.include_documentation(contact_address_doc)
v1.push()
