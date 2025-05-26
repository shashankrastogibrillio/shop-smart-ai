def apply_filters(retriever, filters):
    if not filters:
        return retriever
    retriever.search_kwargs.update({
        "filter": filters
    })
    return retriever
