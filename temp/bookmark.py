<!-- In post_detail.html or wherever you show posts -->
<form action="{% url 'toggle_bookmark' post.id %}" method="post">
    {% csrf_token %}
    <button type="submit">
        {% if post in request.user.bookmarks.all.values_list('post', flat=True) %}
            🔖 Bookmarked
        {% else %}
            📑 Bookmark
        {% endif %}
    </button>
</form>
