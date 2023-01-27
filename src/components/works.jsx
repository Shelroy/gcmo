import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import worksData from '../Services/worksData';
import Image from 'react-bootstrap/Image'
import Pagination from 'react-bootstrap/Pagination';

let active = 2;
let items = [];
for (let number = 1; number <= 5; number++) {
  items.push(
    <Pagination.Item key={number} active={number === active}>
      {number}
    </Pagination.Item>,
  );
}

export default function AppWorks(){
    return(
        <section id="works" className='block works-block'>
            <div className="title-holder">
                <h2>Our Works</h2>
                <div className="subtitle">Our Awesome Works</div>
            </div>
        
    <Container fluid>
    <Row className='portfoliolist'>
        {worksData.map(work=>{
            return(
                <Col sm={3} key={work.id}>

                <div className="portfolio-wrapper">
        
                    <a href={work.link} className="img-fluid">
                        <Image src={work.image} />
                        <div className='label text-center'>
                            <h3>{work.title}</h3>
                            <p>{work.subtitle}</p>
                        </div>
                    </a>
                </div>
              </Col>

            )


        })}

    </Row>
    <Pagination size="sm">{items}</Pagination>

  </Container>
  </section>
    )



}