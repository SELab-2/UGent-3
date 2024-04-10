export const PageTitle = ({ title, defaultTitle, className }: {title:string,defaultTitle:string,className:string}) => {

  return (
    <span className={className}>
      {!title ? (
        <span>{defaultTitle}</span>
      ) : typeof title === 'string' ? (
        <span>{title}</span>
      ) : (
        title
      )}
    </span>
  );
};