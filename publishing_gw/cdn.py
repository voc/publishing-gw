import logging
import paramiko
import urllib
from os import path, environ as env

ssh = None
sftp = None


def connect_ssh():
    global ssh, sftp
    logging.info("Establishing SSH connection")
    ssh = paramiko.SSHClient()
    logging.getLogger("paramiko").setLevel(logging.ERROR)
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host = env.get("SFTP_UPLOAD_HOST", "upload.media.ccc.de")
    try:
        ssh.connect(
            host,
            username=env.get("SFTP_UPLOAD_USER", "cdn-app"),
        )
    except paramiko.AuthenticationException as e:
        raise Exception(f"Authentication failed. Please check credentials {e}") from e
    except paramiko.BadHostKeyException:
        raise Exception("Bad host key. Check your known_hosts file")
    except paramiko.SSHException as e:
        raise Exception(f"SSH negotiation failed {e}") from e

    sftp = ssh.open_sftp()
    logging.info(f"SSH connection established to {host}")



def upload_file(file, target):
    # check if ssh connection is open
    if ssh is None:
        connect_ssh()

    try:
        print("  uploading {} to {}".format(file.filename, target))
        try:
            sftp.mkdir(path.dirname(target))
        except:
            pass
        with sftp.open(target, "w", 32768) as fh:
            while True:
                chunk = file.file.read(32768)
                if not chunk:
                    break
                fh.write(chunk)
    except paramiko.SSHException as e:
        raise Exception(f"could not upload WebVTT because of SSH problem {e}") from e
    except IOError as e:
        raise Exception(f"could not upload WebVTT because of {e}") from e


def upload_from_url(url, target):
    # check if ssh connection is open
    if ssh is None:
        connect_ssh()

    try:
        with urllib.request.urlopen(url) as df:
            print("  uploading {} to {}".format(url, target))
            try:
                sftp.mkdir(path.dirname(target))
            except:
                pass
            with sftp.open(target, "w", 32768) as fh:
                while True:
                    chunk = df.read(32768)
                    if not chunk:
                        break
                    fh.write(chunk)
    except paramiko.SSHException as e:
        raise Exception(f"could not upload WebVTT because of SSH problem {e}") from e
    except IOError as e:
        raise Exception(f"could not upload WebVTT because of {e}") from e
