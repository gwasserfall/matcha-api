from pymysql.err import IntegrityError
from models import Model, Field

class Image(Model):

    table_name = "images"

    id = Field(int, modifiable=False)
    user_id = Field(int)
    image64 = Field(str)
    is_primary = Field(bool)
    image_type = Field(str)

    def before_save(self):
        with self.db.cursor() as c:
            c.execute("""SELECT COUNT(*) as image_count FROM images WHERE user_id=%s""", (self.user_id))
            result = c.fetchone()
            if result.get("image_count", 0) >= 5 and not self.id:
                raise Exception("Cannot upload image, you already have 5. Please delete an image and reupload.")