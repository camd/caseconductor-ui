from ..builder import ListBuilder



attachments = ListBuilder(
    "attachment",
    "attachments",
    "Attachment",
    {
        "name": "Default Attachment",
        "description": "Description",
        "url": "http://www.example.com",
        "size": "10",
        "attachmentTypeId": 8,
        }
    )
