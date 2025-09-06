from datetime import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

follows: Table = db.Table(
    "follows",
    db.Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
    db.Column("followed_id", Integer, ForeignKey("user.id"), primary_key=True),
    db.Column("created_at", DateTime, nullable=False),
)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    profile: Mapped["Profile"] = relationship(
        back_populates="user", uselist=False)
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

    following: Mapped[List["User"]] = relationship(
        "User",
        secondary=follows,
        primaryjoin=lambda: User.id == follows.c.follower_id,
        secondaryjoin=lambda: User.id == follows.c.followed_id,
        back_populates="followers",
    )
    followers: Mapped[List["User"]] = relationship(
        "User",
        secondary=follows,
        primaryjoin=lambda: User.id == follows.c.followed_id,
        secondaryjoin=lambda: User.id == follows.c.follower_id,
        back_populates="following",
    )


class Profile(db.Model):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    biography: Mapped[str] = mapped_column(Text, nullable=True)
    facebook: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), unique=True, nullable=False)
    user: Mapped["User"] = relationship(back_populates="profile")


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(220), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")

    medias: Mapped[List["Media"]] = relationship(back_populates="post")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="medias")


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
