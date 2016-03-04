from sshtunnel import SSHTunnelForwarder
import MySQLdb as mdb


def define_ssh_tunnel(db_config,server_host):
    """Define SSH tunnel"""
    
    ssh_tunnel = SSHTunnelForwarder(
        (db_config['ssh_host']),
        ssh_username=db_config['ssh_user'],
        ssh_private_key =db_config['ssh_key'],
        remote_bind_address=(server_host, 3306)
    )
    
    return ssh_tunnel


def open_db_connection(db_config,ssh_tunnel):
    """Start SSH tunnels"""
    
    local_port = ssh_tunnel.local_bind_port
    connection = mdb.connect('127.0.0.1',db_config['user'],db_config['pw'],'ebdb',local_port)
    
    return connection