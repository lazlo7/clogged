from collections.abc import Iterable
from clogged.post.models import Post, PostTag, TaggedPost
from sqlalchemy import select, func
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession


async def match_tag_strings(tags: Iterable[str], db: AsyncSession) -> dict[int, str]:
    """Returns a dictionary of tag ids mapped to tag names by the given tag names."""
    query = select(PostTag).where(PostTag.name.in_(tags))
    result = await db.execute(query)
    return {tag.id: tag.name for tag, in result}


async def enrich_with_post_tags(query: Select) -> Select:
    """Enriches the given query with post tags."""
    return (query
            .add_columns(func.array_agg(PostTag.name).label("tags"))
            .join(TaggedPost, Post.id == TaggedPost.post_id)
            .join(PostTag, TaggedPost.tag_id == PostTag.id)
            .group_by(Post.id)
    )
