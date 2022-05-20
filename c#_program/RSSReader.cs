using System.Xml;
using System.Net;

namespace newsPortal
{
    class RSSReader
    {
        public List<string> Read(string url)
        {
            List<string> links = new List<string>();
            WebRequest request = WebRequest.Create(url);

            WebResponse response = request.GetResponse();
            XmlDocument doc = new XmlDocument();
            try
            {
                doc.Load(response.GetResponseStream());
                XmlElement rssElem = doc["rss"];
                if (rssElem == null)
                {
                    return links;
                }
                XmlElement chanElem = rssElem["channel"];
                XmlNodeList itemElems = rssElem["channel"].GetElementsByTagName("item");
                if (chanElem != null)
                {
                    foreach (XmlElement itemElem in itemElems)
                    {
                        links.Add(itemElem["link"].InnerText);
                    }
                }
            }
            catch (XmlException) { }

            return links;
        }
    }
}