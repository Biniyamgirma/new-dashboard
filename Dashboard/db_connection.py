from sqlalchemy import create_engine
import streamlit as st

## hh
@st.cache_resource
def create_db_engine():
    """Create and return a SQLAlchemy engine for MariaDB."""
    # Update with your actual database credentials
    user = "analyst"
    password = "a66ed8f80492a2cfd6c03f817b3be1eb"  # Replace with the actual password
    host = "database-production-large-cluster.cluster-ro-cbiml1hzpsyo.eu-west-1.rds.amazonaws.com"
    port = 3306
    database = "beu"

    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)
    return engine
