def test_setup(app , db):
    """Set up the testing enviroment variances"""
    # Use test database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookyourservices_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    app.config['TESTING'] = True
    app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    db.drop_all()
    db.create_all()