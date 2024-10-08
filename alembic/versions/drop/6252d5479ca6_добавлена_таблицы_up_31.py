"""Добавлена таблицы UP:31

Revision ID: 6252d5479ca6
Revises: 
Create Date: 2024-08-30 10:22:43.345633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6252d5479ca6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('middle_name', sa.String(), nullable=False),
    sa.Column('birth_year', sa.Date(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('inn', sa.BigInteger(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('job_title', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('roles', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_table('user_action_history',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('action', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('details', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_region_id'), 'region', ['id'], unique=False)
    op.create_index(op.f('ix_region_title'), 'region', ['title'], unique=True)
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_departments_id'), 'departments', ['id'], unique=False)
    op.create_index(op.f('ix_departments_title'), 'departments', ['title'], unique=True)
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_title'), 'categories', ['title'], unique=True)
    op.create_table('type_selections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_type_selections_title'), 'type_selections', ['title'], unique=True)
    op.create_table('questions',
    sa.Column('question_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('type_select_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['type_select_id'], ['type_selections.id'], ),
    sa.PrimaryKeyConstraint('question_id')
    )
    op.create_index(op.f('ix_questions_question_id'), 'questions', ['question_id'], unique=False)
    op.create_table('answers',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('question_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answers_id'), 'answers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_answers_id'), table_name='answers')
    op.drop_table('answers')
    op.drop_index(op.f('ix_questions_question_id'), table_name='questions')
    op.drop_table('questions')
    op.drop_index(op.f('ix_type_selections_title'), table_name='type_selections')
    op.drop_table('type_selections')
    op.drop_index(op.f('ix_categories_title'), table_name='categories')
    op.drop_table('categories')
    op.drop_index(op.f('ix_departments_title'), table_name='departments')
    op.drop_index(op.f('ix_departments_id'), table_name='departments')
    op.drop_table('departments')
    op.drop_index(op.f('ix_region_title'), table_name='region')
    op.drop_index(op.f('ix_region_id'), table_name='region')
    op.drop_table('region')
    op.drop_table('user_action_history')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
