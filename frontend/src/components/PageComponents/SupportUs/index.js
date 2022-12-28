import {
  SingleElementContainer,
  ColumnContainerBasic,
  GraphicContainer,
  GraphicImg,
} from '../../Common/ContainerElements';
import { FormTitle } from '../../Common/FormElements';
import { ExternalLink } from '../../Common/UserContentElements';
import { AboutUsText } from '../AboutUs/AboutUsElements';

import graphic from '../../../images/support_us.jpg';

const SupportUs = () => {
  return (
    <>
      <SingleElementContainer>
        <ColumnContainerBasic>
          <GraphicContainer>
            <GraphicImg src={graphic} />
          </GraphicContainer>
          <FormTitle>Support</FormTitle>
          <AboutUsText>
            If you found a bug or have an idea,
            send us a message on:
            <ExternalLink
              href='https://github.com/vkiguta/seo-saver'
              target='_blank'>
              https://github.com/vkiguta/seo-saver
            </ExternalLink>
          </AboutUsText>
        </ColumnContainerBasic>
      </SingleElementContainer>
    </>
  );
};

export default SupportUs;
