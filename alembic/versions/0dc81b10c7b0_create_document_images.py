"""Create document_images

Revision ID: 0dc81b10c7b0
Revises: e0508c3db279
Create Date: 2022-05-19 23:23:54.001776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dc81b10c7b0'
down_revision = 'e0508c3db279'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_manifests_id', table_name='manifests')
    op.drop_table('manifests')
    op.drop_index('ix_passengers_date_joined', table_name='passengers')
    op.drop_index('ix_passengers_email', table_name='passengers')
    op.drop_index('ix_passengers_first_name', table_name='passengers')
    op.drop_index('ix_passengers_gender', table_name='passengers')
    op.drop_index('ix_passengers_id', table_name='passengers')
    op.drop_index('ix_passengers_last_name', table_name='passengers')
    op.drop_index('ix_passengers_next_of_kin_first_name', table_name='passengers')
    op.drop_index('ix_passengers_next_of_kin_last_name', table_name='passengers')
    op.drop_index('ix_passengers_next_of_kin_phone_no', table_name='passengers')
    op.drop_index('ix_passengers_phone_no_1', table_name='passengers')
    op.drop_index('ix_passengers_phone_no_2', table_name='passengers')
    op.drop_index('ix_passengers_title', table_name='passengers')
    op.drop_table('passengers')
    op.drop_index('ix_ratings_id', table_name='ratings')
    op.drop_index('ix_ratings_rating', table_name='ratings')
    op.drop_index('ix_ratings_timestamp', table_name='ratings')
    op.drop_table('ratings')
    op.drop_index('ix_locations_current_latitude', table_name='locations')
    op.drop_index('ix_locations_current_longitude', table_name='locations')
    op.drop_index('ix_locations_departure_terminal', table_name='locations')
    op.drop_index('ix_locations_destination_terminal', table_name='locations')
    op.drop_index('ix_locations_id', table_name='locations')
    op.drop_index('ix_locations_timestamp', table_name='locations')
    op.drop_table('locations')
    op.drop_index('ix_document_images_id', table_name='document_images')
    op.drop_table('document_images')
    op.drop_table('manifest_passengers')
    op.drop_index('ix_vehicles_color', table_name='vehicles')
    op.drop_index('ix_vehicles_id', table_name='vehicles')
    op.drop_index('ix_vehicles_maintenance_due_date', table_name='vehicles')
    op.drop_index('ix_vehicles_make', table_name='vehicles')
    op.drop_index('ix_vehicles_model', table_name='vehicles')
    op.drop_index('ix_vehicles_reg_id', table_name='vehicles')
    op.drop_index('ix_vehicles_status', table_name='vehicles')
    op.drop_index('ix_vehicles_today_trip_count', table_name='vehicles')
    op.drop_index('ix_vehicles_type', table_name='vehicles')
    op.drop_table('vehicles')
    op.drop_index('ix_documents_document_expiry_date', table_name='documents')
    op.drop_index('ix_documents_document_no', table_name='documents')
    op.drop_index('ix_documents_document_type', table_name='documents')
    op.drop_index('ix_documents_id', table_name='documents')
    op.drop_table('documents')
    op.drop_index('ix_users_account_no', table_name='users')
    op.drop_index('ix_users_bank', table_name='users')
    op.drop_index('ix_users_bvn', table_name='users')
    op.drop_index('ix_users_date_joined', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_employee_id', table_name='users')
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_gender', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_last_login', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_index('ix_users_level', table_name='users')
    op.drop_index('ix_users_marital_status', table_name='users')
    op.drop_index('ix_users_middle_name', table_name='users')
    op.drop_index('ix_users_nationality', table_name='users')
    op.drop_index('ix_users_next_of_kin_first_name', table_name='users')
    op.drop_index('ix_users_next_of_kin_last_name', table_name='users')
    op.drop_index('ix_users_next_of_kin_phone_no', table_name='users')
    op.drop_index('ix_users_password', table_name='users')
    op.drop_index('ix_users_phone_no_1', table_name='users')
    op.drop_index('ix_users_phone_no_2', table_name='users')
    op.drop_index('ix_users_status', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_reports_detail', table_name='reports')
    op.drop_index('ix_reports_id', table_name='reports')
    op.drop_index('ix_reports_timestamp', table_name='reports')
    op.drop_table('reports')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reports',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('detail', sa.VARCHAR(length=255), nullable=True),
    sa.Column('vehicle_id', sa.INTEGER(), nullable=True),
    sa.Column('passenger_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['passenger_id'], ['passengers.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_reports_timestamp', 'reports', ['timestamp'], unique=False)
    op.create_index('ix_reports_id', 'reports', ['id'], unique=False)
    op.create_index('ix_reports_detail', 'reports', ['detail'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('employee_id', sa.VARCHAR(), nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('middle_name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('password', sa.VARCHAR(), nullable=True),
    sa.Column('phone_no_1', sa.VARCHAR(), nullable=True),
    sa.Column('phone_no_2', sa.VARCHAR(), nullable=True),
    sa.Column('gender', sa.VARCHAR(), nullable=True),
    sa.Column('marital_status', sa.VARCHAR(), nullable=True),
    sa.Column('nationality', sa.VARCHAR(), nullable=True),
    sa.Column('next_of_kin_first_name', sa.VARCHAR(), nullable=True),
    sa.Column('next_of_kin_last_name', sa.VARCHAR(), nullable=True),
    sa.Column('next_of_kin_phone_no', sa.VARCHAR(), nullable=True),
    sa.Column('level', sa.VARCHAR(), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('last_login', sa.VARCHAR(), nullable=True),
    sa.Column('bank', sa.VARCHAR(), nullable=True),
    sa.Column('account_no', sa.VARCHAR(), nullable=True),
    sa.Column('bvn', sa.VARCHAR(), nullable=True),
    sa.Column('date_joined', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_status', 'users', ['status'], unique=False)
    op.create_index('ix_users_phone_no_2', 'users', ['phone_no_2'], unique=False)
    op.create_index('ix_users_phone_no_1', 'users', ['phone_no_1'], unique=False)
    op.create_index('ix_users_password', 'users', ['password'], unique=False)
    op.create_index('ix_users_next_of_kin_phone_no', 'users', ['next_of_kin_phone_no'], unique=False)
    op.create_index('ix_users_next_of_kin_last_name', 'users', ['next_of_kin_last_name'], unique=False)
    op.create_index('ix_users_next_of_kin_first_name', 'users', ['next_of_kin_first_name'], unique=False)
    op.create_index('ix_users_nationality', 'users', ['nationality'], unique=False)
    op.create_index('ix_users_middle_name', 'users', ['middle_name'], unique=False)
    op.create_index('ix_users_marital_status', 'users', ['marital_status'], unique=False)
    op.create_index('ix_users_level', 'users', ['level'], unique=False)
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)
    op.create_index('ix_users_last_login', 'users', ['last_login'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_gender', 'users', ['gender'], unique=False)
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    op.create_index('ix_users_employee_id', 'users', ['employee_id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.create_index('ix_users_date_joined', 'users', ['date_joined'], unique=False)
    op.create_index('ix_users_bvn', 'users', ['bvn'], unique=False)
    op.create_index('ix_users_bank', 'users', ['bank'], unique=False)
    op.create_index('ix_users_account_no', 'users', ['account_no'], unique=False)
    op.create_table('documents',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('document_type', sa.VARCHAR(), nullable=True),
    sa.Column('document_no', sa.VARCHAR(), nullable=True),
    sa.Column('document_expiry_date', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_documents_id', 'documents', ['id'], unique=False)
    op.create_index('ix_documents_document_type', 'documents', ['document_type'], unique=False)
    op.create_index('ix_documents_document_no', 'documents', ['document_no'], unique=False)
    op.create_index('ix_documents_document_expiry_date', 'documents', ['document_expiry_date'], unique=False)
    op.create_table('vehicles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('reg_id', sa.VARCHAR(length=20), nullable=True),
    sa.Column('type', sa.VARCHAR(length=9), nullable=True),
    sa.Column('make', sa.VARCHAR(length=20), nullable=True),
    sa.Column('model', sa.VARCHAR(length=50), nullable=True),
    sa.Column('color', sa.VARCHAR(length=20), nullable=True),
    sa.Column('today_trip_count', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.VARCHAR(length=14), nullable=True),
    sa.Column('maintenance_due_date', sa.VARCHAR(), nullable=True),
    sa.Column('timestamp', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_vehicles_type', 'vehicles', ['type'], unique=False)
    op.create_index('ix_vehicles_today_trip_count', 'vehicles', ['today_trip_count'], unique=False)
    op.create_index('ix_vehicles_status', 'vehicles', ['status'], unique=False)
    op.create_index('ix_vehicles_reg_id', 'vehicles', ['reg_id'], unique=False)
    op.create_index('ix_vehicles_model', 'vehicles', ['model'], unique=False)
    op.create_index('ix_vehicles_make', 'vehicles', ['make'], unique=False)
    op.create_index('ix_vehicles_maintenance_due_date', 'vehicles', ['maintenance_due_date'], unique=False)
    op.create_index('ix_vehicles_id', 'vehicles', ['id'], unique=False)
    op.create_index('ix_vehicles_color', 'vehicles', ['color'], unique=False)
    op.create_table('manifest_passengers',
    sa.Column('manifest_id', sa.INTEGER(), nullable=False),
    sa.Column('passenger_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['manifest_id'], ['manifests.id'], ),
    sa.ForeignKeyConstraint(['passenger_id'], ['passengers.id'], ),
    sa.PrimaryKeyConstraint('manifest_id', 'passenger_id')
    )
    op.create_table('document_images',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_document_images_id', 'document_images', ['id'], unique=False)
    op.create_table('locations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('departure_terminal', sa.VARCHAR(length=50), nullable=True),
    sa.Column('destination_terminal', sa.VARCHAR(length=50), nullable=True),
    sa.Column('current_trip', sa.BOOLEAN(), nullable=True),
    sa.Column('current_latitude', sa.VARCHAR(length=20), nullable=True),
    sa.Column('current_longitude', sa.VARCHAR(length=20), nullable=True),
    sa.Column('started_trip', sa.BOOLEAN(), nullable=True),
    sa.Column('ended_trip', sa.BOOLEAN(), nullable=True),
    sa.Column('timestamp', sa.VARCHAR(), nullable=True),
    sa.Column('manifest_id', sa.INTEGER(), nullable=True),
    sa.Column('vehicle_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['manifest_id'], ['manifests.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_locations_timestamp', 'locations', ['timestamp'], unique=False)
    op.create_index('ix_locations_id', 'locations', ['id'], unique=False)
    op.create_index('ix_locations_destination_terminal', 'locations', ['destination_terminal'], unique=False)
    op.create_index('ix_locations_departure_terminal', 'locations', ['departure_terminal'], unique=False)
    op.create_index('ix_locations_current_longitude', 'locations', ['current_longitude'], unique=False)
    op.create_index('ix_locations_current_latitude', 'locations', ['current_latitude'], unique=False)
    op.create_table('ratings',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('rating', sa.INTEGER(), nullable=True),
    sa.Column('vehicle_id', sa.INTEGER(), nullable=True),
    sa.Column('passenger_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['passenger_id'], ['passengers.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ratings_timestamp', 'ratings', ['timestamp'], unique=False)
    op.create_index('ix_ratings_rating', 'ratings', ['rating'], unique=False)
    op.create_index('ix_ratings_id', 'ratings', ['id'], unique=False)
    op.create_table('passengers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('gender', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('phone_no_1', sa.VARCHAR(), nullable=True),
    sa.Column('phone_no_2', sa.VARCHAR(), nullable=True),
    sa.Column('next_of_kin_first_name', sa.VARCHAR(), nullable=True),
    sa.Column('next_of_kin_last_name', sa.VARCHAR(), nullable=True),
    sa.Column('next_of_kin_phone_no', sa.VARCHAR(), nullable=True),
    sa.Column('date_joined', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_passengers_title', 'passengers', ['title'], unique=False)
    op.create_index('ix_passengers_phone_no_2', 'passengers', ['phone_no_2'], unique=False)
    op.create_index('ix_passengers_phone_no_1', 'passengers', ['phone_no_1'], unique=False)
    op.create_index('ix_passengers_next_of_kin_phone_no', 'passengers', ['next_of_kin_phone_no'], unique=False)
    op.create_index('ix_passengers_next_of_kin_last_name', 'passengers', ['next_of_kin_last_name'], unique=False)
    op.create_index('ix_passengers_next_of_kin_first_name', 'passengers', ['next_of_kin_first_name'], unique=False)
    op.create_index('ix_passengers_last_name', 'passengers', ['last_name'], unique=False)
    op.create_index('ix_passengers_id', 'passengers', ['id'], unique=False)
    op.create_index('ix_passengers_gender', 'passengers', ['gender'], unique=False)
    op.create_index('ix_passengers_first_name', 'passengers', ['first_name'], unique=False)
    op.create_index('ix_passengers_email', 'passengers', ['email'], unique=False)
    op.create_index('ix_passengers_date_joined', 'passengers', ['date_joined'], unique=False)
    op.create_table('manifests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('driver_id', sa.INTEGER(), nullable=True),
    sa.Column('vehicle_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_manifests_id', 'manifests', ['id'], unique=False)
    # ### end Alembic commands ###
