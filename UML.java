class FileSystem { 
   class Folder { 
      private int id; 
      public String name; 
      public File file //Composition 
      } 
   class File { 
      public Folder folder 
      public String name; 
      public Content content //Composition 
      } 
   class Content { 
      public File file 
      public String blob; 
      } 
   } 
