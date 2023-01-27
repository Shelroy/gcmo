import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

export default function AppContact(){
    return(
        <section id="contact" className='block contact-block'>
      
          <Container fluid>
            <div className="title-holder">
                <h2>Contact Us</h2>
                <div className="subtitle">Drop us a line</div>
            </div>
    
      <Form className='contact-form'>
      <Row>
        <Col sm={4}>
          <Form.Control type ="text" placeholder="Enter your full name" />
        </Col>
        <Col sm={4}>
          <Form.Control type = "email" placeholder="Enter your email address" />
        </Col >
        <Col sm={4}>
          <Form.Control type = "tel" placeholder="Enter your contact number" />
        </Col >
        
       
      </Row>
      <Row>
            <Col sm={12}>
            <Form.Control as="textarea" placeholder="Enter a message" />
            </Col>
        </Row>


      <div className='btn-holder'>
        <Button type="submit">Submit</Button>
            
            </div>
    </Form>
    
    </Container>
    <div className="google-map">
    <iframe title="map" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d22410.888263394576!2d-58.15306722912908!3d6.803541766985447!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8dafefaf60d8c2b3%3A0x72c2a4440b00eb7d!2sGeorgetown!5e0!3m2!1sen!2sgy!4v1674678460228!5m2!1sen!2sgy"  allowFullScreen="" loading="lazy" referrerPolicy="no-referrer-when-downgrade"></iframe>
    </div>
    <Container fluid>
        <div className="contact-info">
            <ul>
                <li>
                    <i className="fas  fa-envelope"></i>
                    jleegcmc@gmail.com
                </li>
                <li>
                    <i className="fas  fa-phone"></i>
                    +592-609-7398

                </li>
                <li>
                    <i className="fas  fa-map-marker-alt"></i>
                    Georgetown Guyana
                </li>
            </ul>
        </div>

    </Container>
    </section>
       
    )
}