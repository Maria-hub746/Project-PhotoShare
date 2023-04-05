import io
import cloudinary

from cloudinary.uploader import upload
from starlette.responses import StreamingResponse

from sqlalchemy.orm import Session
from src.conf.config import init_cloudinary, qr
from src.tramsform_schemas import TransformCircleModel, TransformEffectModel, TransformResizeModel, TransformTextModel

from src.database.models import Post, User


async def transform_metod_circle(post_id: int, body: TransformCircleModel, user: User, db: Session) -> Post | None:
    post= db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()
    if post:
        upload(post.image_url, public_id=str(post.id))
        transformation = []
        if body.height and body.width:
            transformation.append(
            {'gravity': "face", 'height': f"{body.height}", 'width': f"{body.width}", 'crop': "thumb"},
            {'radius': "max"}
            )
            init_cloudinary()
            url = cloudinary.CloudinaryImage(str(post.id)).build_url(
                transformation=transformation
            )
            post.image_url = url
            db.commit()

    return post


async def transform_metod_effect(post_id: int, body: TransformEffectModel, user: User, db: Session) -> Post | None:
    post= db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()
    if post:
        upload(post.image_url, public_id=str(post.id))
        transformation = []
        effect = ""
        if body.art_audrey:
            effect = "art:audrey"
        if body.art_zorro:
            effect = "art:zorro"
        if body.blur:
            effect = "blur:300"
        if body.cartoonify:
            effect = "cartoonify"
        if effect:
            transformation.append({"effect": f"{effect}"})
            init_cloudinary()
            url = cloudinary.CloudinaryImage(str(post.id)).build_url(
                transformation=transformation
            )
            post.image_url = url
            db.commit()

    return post


async def transform_metod_resize(post_id: int, body: TransformResizeModel, user: User, db: Session) -> Post | None:
    post= db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()
    if post:
        upload(post.image_url, public_id=str(post.id))
        transformation = []
        crop = ""
        if body.crop:
            crop = "crop"
        if body.scale:
            crop = "scale"
        if body.fill:
            crop = "fill"
        if body.pad:
            crop = "pad"
        if crop:
            transformation.append(
            {"gravity": "auto", 'height': f"{body.height}", 'width': f"{body.width}", 'crop': f"{crop}"}
            )
            init_cloudinary()
            url = cloudinary.CloudinaryImage(str(post.id)).build_url(
                transformation=transformation
            )
            post.image_url = url
            db.commit()

    return post


async def transform_metod_text(post_id: int, body: TransformTextModel, user: User, db: Session) -> Post | None:
    post= db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()
    if post:
        upload(post.image_url, public_id=str(post.id))
        transformation = []
        if body.text:
            transformation.append(
            {'color': "#FFFF00", 'overlay': {'font_family': "Times", 'font_size': f"{body.font_size}", 'font_weight': "bold", 'text': f"{body.text}"}}, {'flags': "layer_apply", 'gravity': "south", 'y': 20}
            )
            init_cloudinary()
            url = cloudinary.CloudinaryImage(str(post.id)).build_url(
                transformation=transformation
            )
            post.image_url = url
            db.commit()

    return post


async def show_qr(post_id: int, user: User, db: Session) -> Post | None:
    post= db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()
    if post:
        if post.image_url:
            img = qr.make(post.image_url)
            buf = io.BytesIO()
            img.save(buf)
            buf.seek(0)
            return StreamingResponse(buf, media_type="image/jpeg")    

    return post
