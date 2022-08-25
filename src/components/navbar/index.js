
import './navbar.css';
import logo from '../../assets/image/svg/logo.svg'

function Navbar() {

    return (
        <header>
            <nav className="navbar fixed-top ">
                <div className="container">
                    <a className="navbar-brand mb-0 h1"><img src={logo} alt="imagem da logo" /></a>


                </div>

            </nav>
        </header>


    );
}

export default Navbar;
