
import { useNavigate, useParams } from "react-router-dom";
import './begin.css';
import bkg from "../../assets/image/bkg/bkgBegin.png"

function Begin() {
    const navigate = useNavigate();
    return (
        <section className="begin-corpo">

            <div className="begin">
                <div className="container">
                    <div className="row">
                        <div className="col-lg-5 body-begin">
                            <div className="apresentation">
                                <div className="title">
                                    <h2>
                                        Assita junto virtualmente
                                    </h2>
                                </div>
                                <div className="text">
                                    <p>
                                        Crie uma sala, compartilhe o ID da sala com seus amigos e assista com todos!
                                    </p>
                                </div>
                                <div className="but" onClick={() => { navigate("entrar") }}>
                                    <a className='bt' ><span className="bol"></span> Começar</a>
                                </div>

                            </div>

                        </div>
                        <div className="col-lg-7 body-begin image">
                            <img src={bkg} className="img-fluid" alt="imagem de fundo do inicio" />
                        </div>

                    </div>
                </div>
            </div>


            <div className="service">
                <div className="container">
                    <div className="title">
                        <h3>Serviços</h3>

                    </div>

                    <div className="sml">
                        <small>Disponiveis em todo o  site</small>

                    </div>
                </div>
                <div className="container">
                    <div className="row">
                        <div className="col-lg-5 body-service">
                            <div className="img-service"><i className="fa-solid fa-tv"></i></div>
                            <div className="title-service"><h4>Assita um video</h4></div>
                            <div className="text-service container"><p>
                                Assista ao conteúdo de vídeo com todos de forma síncronizada. Cada Membro pode iniciar qualquer vídeo, iniciar, pausar e buscar tempo de forma síncrona.
                            </p>
                            </div>
                        </div>
                        <div className="col-lg-5 body-service">
                            <div className="img-service"><i className="fa-regular fa-message"></i></div>
                            <div className="title-service"><h5>Chat em tempo real</h5></div>
                            <div className="text-service container"><p>
                                Adicione quantas pessoas quiser à sua sala.Assistir Juntos e conversar com todos eles. Cada membro pode enviar e ler todas as mensagens.
                            </p> </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Begin;
