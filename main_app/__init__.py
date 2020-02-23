from flask import Blueprint, render_template, session, request, redirect, url_for
import app_config

from .forms import Profile_Edit_Form, Create_Text_Post_Form, Create_Link_Post_Form

import datetime

main_app = Blueprint('main_app', __name__, template_folder = 'templates')


def get_user():
    if 'email' in session:
        return app_config.db.get_user_by_email(session['email'])
    else:
        return None


@main_app.route('/')
@main_app.route('/index/')
def index():
    return render_template('/semi_static/index.html', title = 'Home', user = get_user())


@main_app.route('/home/')
def home():
    user = get_user()
    if user:
        return render_template('home.html', title = 'Home', user = user)
    else:
        return redirect(url_for('main_app.boards'))



@main_app.route('/my_account/')
def my_account():
    user = get_user()
    if user:
        return render_template('my_account.html', title = 'My Account', user = user)
    else:
        return '404 Page Not Found'



@main_app.route('/contact/')
def contact():
    return render_template('/semi_static/contact.html', title = 'Contact', user = get_user())


#Shows all the Boards on the website.
@main_app.route('/board/')
def boards():
    return render_template('boards.html', title = 'All Boards', user = get_user(), boards = app_config.db.get_all_boards())



#Shows all the Sub Boards in that Board.
@main_app.route('/board/<board_name>/')
def sub_boards(board_name):
    board = app_config.db.get_board_by_name(board_name)
    if board:
        return render_template('sub_boards.html', title = board['name'], user = get_user(), board = board, sub_boards = app_config.db.get_sub_boards_by_board_id(board['id']))
    else:
        return '404 Page Not Found'



#Shows all the Posts on a given Sub Board.
@main_app.route('/board/<board_name>/<sub_board_name>/')
def posts(board_name, sub_board_name):
    board = app_config.db.get_board_by_name(board_name)
    sub_board = app_config.db.get_sub_board_by_board_id_and_name(board['id'], sub_board_name)
    if sub_board:
        return render_template('posts.html', title = f'{board["name"]} - {sub_board["name"]}',
            user = get_user(), board = board, sub_board = sub_board, posts = app_config.db.get_posts_by_sub_board_id(sub_board['id']), db = app_config.db)
    else:
        return '404 Page Not Found'



#Show one particular Post.
@main_app.route('/board/<board_name>/<sub_board_name>/<post_id>/')
def post(board_name, sub_board_name, post_id):
    board = app_config.db.get_board_by_name(board_name)
    sub_board = app_config.db.get_sub_board_by_board_id_and_name(board['id'], sub_board_name)
    post = app_config.db.get_post_by_id(post_id)
    if post:
        return render_template('post.html', title = f'{board["name"]} - {sub_board["name"]} - {post["id"]}',
            user = get_user(), board = board, sub_board = sub_board, posts = app_config.db.get_posts_by_sub_board_id(sub_board['id']),
            post = post, comments = app_config.db.get_comments_by_post_id(post_id), db = app_config.db)
    else:
        return '404 Page Not Found'



#Gives user option of what type of post to post.
@main_app.route('/board/<board_name>/<sub_board_name>/create_post/')
def create_post(board_name, sub_board_name):
    user = get_user()
    board = app_config.db.get_board_by_name(board_name)
    sub_board = app_config.db.get_sub_board_by_board_id_and_name(board['id'], sub_board_name)
    if sub_board and user:
        return render_template('create_post.html', title = f'{board["name"]} - {sub_board["name"]} - Create Post',
            user = user, board = board, sub_board = sub_board)
    else:
        return '404 Page Not Found'



#Lets the user create a text post.
@main_app.route('/board/<board_name>/<sub_board_name>/create_text_post/', methods = ['GET', 'POST'])
def create_text_post(board_name, sub_board_name):
        user = get_user()
        board = app_config.db.get_board_by_name(board_name)
        sub_board = app_config.db.get_sub_board_by_board_id_and_name(board['id'], sub_board_name)
        if sub_board and user:
            if request.method == 'POST':
                form = Create_Text_Post_Form(request.form)
                app_config.db.add_post(form.post_title, 0, form.post_content ,datetime.datetime.now().strftime('%H:%M %d-%m-%Y'), user['id'], sub_board['id'])
                return redirect(url_for('main_app.posts', board_name = board_name, sub_board_name = sub_board_name))
            else:
                return render_template('create_text_post.html', title = f'{board["name"]} - {sub_board["name"]} - Create Text Post',
                    user = user, board = board, sub_board = sub_board)
        else:
            return '404 Page Not Found'



#Lets the user create a link post.
@main_app.route('/board/<board_name>/<sub_board_name>/create_link_post/', methods = ['GET', 'POST'])
def create_link_post(board_name, sub_board_name):
        user = get_user()
        board = app_config.db.get_board_by_name(board_name)
        sub_board = app_config.db.get_sub_board_by_board_id_and_name(board['id'], sub_board_name)
        if sub_board and user:
            if request.method == 'POST':
                form = Create_Link_Post_Form(request.form)
                if(form.error):
                    return render_template('create_link_post.html', title = f'{board["name"]} - {sub_board["name"]} - Create Link Post',
                        user = user, board = board, sub_board = sub_board, error_description = form.error_description)
                else:
                    content = f'<a href = \'{form.post_link}\' target = \'_blank\'>{form.post_link }</a>'
                    app_config.db.add_post(form.post_title, 1, content, datetime.datetime.now().strftime('%H:%M %d-%m-%Y'), user['id'], sub_board['id'])
                    return redirect(url_for('main_app.posts', board_name = board_name, sub_board_name = sub_board_name))
            else:
                return render_template('create_link_post.html', title = f'{board["name"]} - {sub_board["name"]} - Create Link Post',
                    user = user, board = board, sub_board = sub_board)
        else:
            return '404 Page Not Found'



@main_app.route('/board/<board_name>/<sub_board_name>/create_image_post/', methods = ['GET', 'POST'])
def create_image_post(board_name, sub_board_name):
    user = get_user()
    board = app_config.db.get_board_by_name(board_name)
    sub_board = app_config.db.get_sub_board_by_board_id_and_name(board['id'], sub_board_name)
    if sub_board and user:
        if request.method == 'POST':
            return redirect(url_for('main_app.posts', board_name = board_name, sub_board_name = sub_board_name))

        else:
            return render_template('/content_creating_templates/create_image_post.html/',
                title = f'{board["name"]} - {sub_board["name"]} - Create Link Post', user = user,
                board = board, sub_board = sub_board)
    else:
        return '404 Page Not Found'



@main_app.route('/<post_id>/create_comment/', methods = ['GET', 'POST'])
def create_comment(post_id):
    user = get_user()
    post = app_config.db.get_post_by_id(post_id)
    if post and user:
        if request.method == 'POST':
            app_config.db.add_comment(request.form['comment'], datetime.datetime.now().strftime('%H:%M %d-%m-%Y'), user['id'], post_id)
            return redirect(url_for('main_app.boards'))
        return render_template('create_comment.html', user = user, post = post)
    else:
        return '404 Page Not Found'



@main_app.route('/<post_id>/like_post/')
def like_post(post_id):
    user = get_user()
    if app_config.db.get_post_by_id(post_id) and user and not app_config.db.get_like_by_post_id_and_user_id(post_id, user['id']):
        app_config.db.add_like(post_id, user['id'])
        return redirect(url_for('main_app.boards'))
    else:
        return '404 Page Not Found'



@main_app.route('/<post_id>/delete_post/')
def delete_post(post_id):
    user = get_user()
    post = app_config.db.get_post_by_id(post_id)
    if user and post:
        if user['id'] == post['owner_id']:
            app_config.db.delete_post(post_id)
            return redirect(url_for('main_app.home'))
        else:
            return 'Permision Denied'
    else:
        return '404 Page Not Found'



@main_app.route('/<post_id>/edit_post/', methods = ['GET', 'POST'])
def edit_post(post_id):
    user = get_user()
    post = app_config.db.get_post_by_id(post_id)
    if user and post:
        if user['id'] == post['owner_id'] and post['type'] == 0:
            if request.method == 'POST':
                app_config.db.update_post_content(request.form['content'], post['id'])
                return redirect(url_for('main_app.home'))
            else:
                return render_template('/content_managing_templates/edit_post.html', title = 'Edit Post', user = user, post = post)
        else:
            return 'Permision Denied'
    else:
        return '404 Page Not Found'



@main_app.route('/setup_profile/', methods = ['GET', 'POST'])
def setup_profile():
    if 'email' in session:
        user = app_config.db.get_user_by_email(session['email'])
        if app_config.db.get_profile_by_user_id(user['id']):
            return redirect(url_for('main_app.edit_profile'))
        if request.method == 'POST':
            form = Profile_Edit_Form(request.form)
            app_config.db.add_profile(form.profile_name, form.profile_bio, form.profile_location, user['id'])
            return redirect(url_for('main_app.home'))
        return render_template('profile_templates/setup_profile.html', title = 'Setup Profile', user = user, profile_name = '')
    else:
        return 'Must be logged in to use this feature.'



@main_app.route('/edit_profile/', methods = ['GET', 'POST'])
def edit_profile():
    return 'LOL'



@main_app.route('/profile/<user_id>')
def view_profile(user_id):
    profile_user = app_config.db.get_user_by_id(user_id)
    profile_data = app_config.db.get_profile_by_user_id(user_id)
    if profile_data:
        return render_template('profile_templates/user_profile.html', title = f'{profile_data["profile_name"]}\'s Profile', profile_data = profile_data,
            profile_user = profile_user, user = get_user())
    else:
        return '404 Page Not Found'
