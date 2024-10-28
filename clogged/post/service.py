from typing import Any
from collections.abc import Iterable
from clogged.post.models import Post, PostTag, TaggedPost
from clogged.post.utils import match_tag_strings, enrich_with_post_tags
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, insert


async def get_post(post_id: int, db: AsyncSession) -> dict[str, Any] | None:
    """Returns the post by the given id or None if post does not exist."""
    query = (
        select(Post)
        .where(Post.id == post_id)
    )
    query = await enrich_with_post_tags(query)
    result = (await db.execute(query)).first()
    if result is None:
        return None
    
    post, tags = result
    post = {
        "id": post.id,
        "poster_id": post.poster_id,
        "title": post.title,
        "created_at": post.created_at,
        "text": post.text,
        "tags": tags
    }

    return post


async def get_latest_posts_info(
    tags: Iterable[str] | None = None,
    *,
    limit: int, 
    offset: int,
    db: AsyncSession
) -> list[dict[str, Any]]:
    """
    Returns a max of `limit` latest posts info containing at least one given tag if any given, 
    offset by `offset` in the format of:

    `{'id': post_id, 'poster_id': poster_id, 'title': title, 'created_at': created_at, 'tags': [tag1, tag2, ...]}`
    """
    # Selecting post info with aggregated post tags.
    query = select(
        Post.id, 
        Post.poster_id, 
        Post.title, 
        Post.created_at 
    )
    query = await enrich_with_post_tags(query)

    if tags is not None:
        tag_ids = (await match_tag_strings(tags, db)).keys()
        query = query.where(TaggedPost.tag_id.in_(tag_ids))
    
    query = (
        query
            .order_by(Post.created_at.desc())
            .limit(limit)
            .offset(offset)
    )

    print(query)

    result = await db.execute(query)
    
    posts = [
        {
            "id": post_id, 
            "poster_id": poster_id, 
            "title": title, 
            "created_at": created_at, 
            "tags": tags
        } 
        for post_id, poster_id, title, created_at, tags in result.all()
    ]
    
    return posts


async def add_post(
    tags: Iterable[str] | None = None,
    *,
    poster_id: int,
    title: str,
    text: str,
    db: AsyncSession,
) -> dict[str, Any]:
    """
    Adds a new post and returns the added post info. Poster with the given `poster_id` is assumed to exist.
    
    Invalid `tags` are ignored.
    """
    post = Post(poster_id=poster_id, title=title, text=text)
    db.add(post)

    if tags is not None:
        matched_tags = await match_tag_strings(tags, db)
        tag_ids = list(matched_tags.keys())
        tags = list(matched_tags.values())
        # Have to commit the post first to get a valid id.
        await db.commit()
        db.add_all(TaggedPost(post_id=post.id, tag_id=tag_id) for tag_id in tag_ids)

    await db.commit()

    post_info = {
        "id": post.id,
        "poster_id": post.poster_id,
        "title": post.title,
        "created_at": post.created_at,
        "tags": tags
    }

    return post_info


async def modify_post(
    new_tags: Iterable[str] | None = None,
    *,
    post_id: int,
    new_title: str,
    new_text: str,
    db: AsyncSession
) -> dict[str, Any] | None:
    """Updates the post with the given post id and returns the updated post info or None if post does not exist."""
    query = select(Post).where(Post.id == post_id)
    query = await enrich_with_post_tags(query)
    result = (await db.execute(query)).first()
    if result is None:
        return None

    post, tags = result
    post.title = new_title
    post.text = new_text

    if new_tags is not None:
        new_matched_tags = await match_tag_strings(new_tags, db)
        new_tag_ids = set(new_matched_tags.keys())
        new_tags = list(new_matched_tags.values())

        # Computing set differences to find optimal way to add/remove tags.
        current_tag_ids = set(tags)
        tags_to_remove = current_tag_ids - new_tag_ids
        tags_to_add = new_tag_ids - current_tag_ids

        if tags_to_remove: 
            tag_remove_query = (
                delete(TaggedPost)
                .where(TaggedPost.post_id == post_id)
                .where(TaggedPost.tag_id.in_(tags_to_remove))
            )
            await db.execute(tag_remove_query)
            
        if tags_to_add:
            db.add_all(TaggedPost(post_id=post_id, tag_id=tag_id) for tag_id in new_tag_ids)

    await db.commit()

    post_info = {
        "id": post.id,
        "poster_id": post.poster_id,
        "title": post.title,
        "created_at": post.created_at,
        "tags": new_tags,
        "text": post.text
    }

    return post_info


async def remove_post(post_id: int, db: AsyncSession) -> dict[str, Any] | None:
    """Removes the post by the given post id and returns the removed post info or None if post does not exist."""
    query = select(Post).where(Post.id == post_id)
    query = await enrich_with_post_tags(query)
    post = (await db.execute(query)).scalar()
    if post is None:
        return None

    removed_post = {
        "id": post.id,
        "poster_id": post.poster_id,
        "title": post.title,
        "created_at": post.created_at,
        "tags": post.tags
    }

    await db.delete(post)

    tag_query = delete(TaggedPost).where(TaggedPost.post_id == post_id)
    await db.execute(tag_query)
    await db.commit()

    return removed_post


async def get_all_tags(db: AsyncSession) -> list[dict[str, str]]:
    """Returns a list of all tags in the format of `{'tag': tag_name}`."""
    query = select(PostTag.name)
    result = await db.execute(query)
    return [{"tag": tag} for tag, in result.all()]


async def add_tag(tag: str, db: AsyncSession) -> dict[str, str] | None:
    """
    Creates a new `tag` and returns it in the format of `{'tag': tag_name}`.
    
    Returns None if the tag already exists.
    """
    if (await match_tag_strings([tag], db)):
        return None

    query = insert(PostTag).values(name=tag)
    await db.execute(query)
    await db.commit()

    result = {"tag": tag}
    return result


async def delete_tag(tag: str, db: AsyncSession) -> dict[str, str] | None:
    """
    Deletes the `tag` and returns it in the format of `{'tag': tag_name}`.
    
    Returns None if the tag does not exist.
    """
    tag_id = (await match_tag_strings([tag], db)).keys()
    if not tag_id:
        return None

    tag_id = next(iter(tag_id))

    query = delete(TaggedPost).where(TaggedPost.tag_id == tag_id)
    await db.execute(query)
    query = delete(PostTag).where(PostTag.id == tag_id)
    await db.execute(query)
    await db.commit()
    
    result = {"tag": tag}
    return result
