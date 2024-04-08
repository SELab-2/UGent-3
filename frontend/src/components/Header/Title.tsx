import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import PropTypes from 'prop-types';

export const Title = (props: TitleProps) => {
  const { defaultTitle, title } = props;
  const [container, setContainer] = useState(() =>
    typeof document !== 'undefined'
      ? document.getElementById('react-admin-title')
      : null
  );

  // on first mount, we don't have the container yet, so we wait for it
  useEffect(() => {
    setContainer(container => {
      const isInTheDom =
                typeof document !== 'undefined' &&
                document.body.contains(container);
      if (container && isInTheDom) return container;
      return typeof document !== 'undefined'
        ? document.getElementById('react-admin-title')
        : null;
    });
  }, []);

  if (!container) return null;

  return createPortal(
    <>{title || defaultTitle}</>,
    container
  );
};

export const TitlePropType = PropTypes.oneOfType([
  PropTypes.string,
  PropTypes.element,
]);

Title.propTypes = {
  defaultTitle: PropTypes.string,
  className: PropTypes.string,
  record: PropTypes.any,
  title: TitlePropType,
};

export interface TitleProps {
    className?: string;
    defaultTitle?: string;
    title?: string;
    preferenceKey?: string;
}