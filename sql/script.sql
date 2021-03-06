USE [master]
GO
/****** Object:  Database [db_projetos]    Script Date: 04/03/2022 08:31:42 ******/
CREATE DATABASE [db_projetos]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'db_projetos', FILENAME = N'/var/opt/mssql/data/db_projetos.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'db_projetos_log', FILENAME = N'/var/opt/mssql/data/db_projetos_Log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [db_projetos] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [db_projetos].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [db_projetos] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [db_projetos] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [db_projetos] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [db_projetos] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [db_projetos] SET ARITHABORT OFF 
GO
ALTER DATABASE [db_projetos] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [db_projetos] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [db_projetos] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [db_projetos] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [db_projetos] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [db_projetos] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [db_projetos] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [db_projetos] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [db_projetos] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [db_projetos] SET  DISABLE_BROKER 
GO
ALTER DATABASE [db_projetos] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [db_projetos] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [db_projetos] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [db_projetos] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [db_projetos] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [db_projetos] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [db_projetos] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [db_projetos] SET RECOVERY FULL 
GO
ALTER DATABASE [db_projetos] SET  MULTI_USER 
GO
ALTER DATABASE [db_projetos] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [db_projetos] SET DB_CHAINING OFF 
GO
ALTER DATABASE [db_projetos] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [db_projetos] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [db_projetos] SET DELAYED_DURABILITY = DISABLED 
GO
EXEC sys.sp_db_vardecimal_storage_format N'db_projetos', N'ON'
GO
ALTER DATABASE [db_projetos] SET QUERY_STORE = OFF
GO
USE [db_projetos]
GO
/****** Object:  User [dev]    Script Date: 04/03/2022 08:31:43 ******/
CREATE USER [dev] WITHOUT LOGIN WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  Table [dbo].[ciclo]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ciclo](
	[id_ciclo] [int] IDENTITY(1,1) NOT NULL,
	[nome_ciclo] [varchar](100) NULL,
	[data_inicio] [date] NULL,
	[data_fim] [date] NULL,
	[descricao] [varchar](1000) NULL,
	[criacao] [date] NULL,
	[alteracao] [date] NULL,
	[ciclo_completo] [char](3) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[cliente]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[cliente](
	[id_cliente] [int] IDENTITY(1,1) NOT NULL,
	[nome_cliente] [varchar](100) NULL,
	[situacao_comercial] [varchar](100) NULL,
	[servico_portfolio] [varchar](100) NULL,
	[descricao] [varchar](1000) NULL,
	[criacao] [date] NULL,
	[alteracao] [date] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[projeto]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[projeto](
	[id_projeto] [int] IDENTITY(1,1) NOT NULL,
	[nome_projeto] [varchar](100) NULL,
	[tipo_projeto] [varchar](100) NULL,
	[nome_cliente] [varchar](100) NULL,
	[lider_projeto] [varchar](100) NULL,
	[categoria_projeto] [varchar](100) NULL,
	[descricao] [varchar](1000) NULL,
	[criacao] [date] NULL,
	[alteracao] [date] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tarefa]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tarefa](
	[id_tarefa] [int] IDENTITY(1,1) NOT NULL,
	[data] [date] NULL,
	[time] [time](7) NULL,
	[nome_tarefa] [varchar](100) NULL,
	[nome_cliente] [varchar](100) NULL,
	[nome_projeto] [varchar](100) NULL,
	[nome_lider] [varchar](100) NULL,
	[ciclo] [varchar](100) NULL,
	[descricao] [varchar](1000) NULL,
	[criacao] [date] NULL,
	[alteracao] [date] NULL,
	[ciclo_completo] [char](3) NULL
) ON [PRIMARY]
GO
/****** Object:  StoredProcedure [dbo].[sp_ciclo]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_ciclo] AS 
    WITH base1 AS (
        SELECT
            nome_ciclo AS ciclo
            , CASE
                WHEN ciclo_completo = 'sim' THEN 1
                ELSE 0
            END AS ciclo_completo
        FROM ciclo
    ),

    base2 AS (
        SELECT 
            ciclo
            , COUNT(ciclo_completo) AS ciclo_completo
        FROM base1
        GROUP BY ciclo
    ) 

    select
        CASE
            WHEN ciclo_completo = 1 THEN MAX(ciclo)
            ELSE '-'
        END AS ciclo
    from base2
    GROUP BY ciclo_completo
GO
/****** Object:  StoredProcedure [dbo].[sp_cliente]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_cliente] AS
    SELECT
        C.nome_cliente
        , C.servico_portfolio
        , P.nome_projeto
    FROM cliente AS C
    INNER JOIN projeto AS P ON P.nome_cliente = C.nome_cliente
    INNER JOIN tarefa AS T ON T.nome_cliente = C.nome_cliente AND T.nome_projeto = P.nome_projeto
    WHERE T.ciclo_completo = 'Não'
    GROUP BY 
        C.nome_cliente
        , C.servico_portfolio
        , P.nome_projeto
GO
/****** Object:  StoredProcedure [dbo].[sp_fatura]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_fatura] AS 
    SELECT 
        COALESCE(CAST((sum( DATEPART(SECOND, time) + 60 * 
                DATEPART(MINUTE, time) + 3600 * 
                DATEPART(HOUR, time ) 
                ) * 0.00833 ) AS INT), 0) AS faturado 
    FROM cliente AS C 
    INNER JOIN projeto AS P ON P.nome_cliente = C.nome_cliente
    INNER JOIN tarefa AS T ON T.nome_cliente = C.nome_cliente AND T.nome_projeto = P.nome_projeto
    WHERE T.ciclo_completo = 'Não'
GO
/****** Object:  StoredProcedure [dbo].[sp_hora]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_hora] AS 
    WITH base AS (
        SELECT 
            CONVERT(varchar(5), DATEADD(ms, SUM(DATEDIFF(ms, '00:00:00.000', time)), '00:00:00.000'), 8) AS time
        FROM cliente AS C 
        INNER JOIN projeto AS P ON P.nome_cliente = C.nome_cliente
        INNER JOIN tarefa AS T ON T.nome_cliente = C.nome_cliente AND T.nome_projeto = P.nome_projeto
        WHERE T.ciclo_completo = 'Não'
    )

    SELECT 
        CASE
            WHEN time IS NULL THEN CONVERT(varchar(5),0)
            ELSE time
        END AS time
    FROM base
GO
/****** Object:  StoredProcedure [dbo].[sp_projeto]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_projeto] AS 
    SELECT 
        P.nome_projeto 
        , COUNT(DISTINCT(nome_tarefa)) AS qtd_tarefa
        , COUNT(nome_tarefa) AS qtd_atividade
    FROM cliente AS C 
    INNER JOIN projeto AS P ON P.nome_cliente = C.nome_cliente
    INNER JOIN tarefa AS T ON T.nome_cliente = C.nome_cliente AND T.nome_projeto = P.nome_projeto
    WHERE T.ciclo_completo = 'Não'
    GROUP BY 
        P.nome_projeto
GO
/****** Object:  StoredProcedure [dbo].[sp_tarefa]    Script Date: 04/03/2022 08:31:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_tarefa] AS (
    SELECT 
        C.nome_cliente
        , servico_portfolio
        , P.nome_projeto 
        , nome_tarefa
        , FORMAT(data, 'dd/MM/yyyy') AS data
        , time
    FROM cliente AS C 
    INNER JOIN projeto AS P ON P.nome_cliente = C.nome_cliente
    INNER JOIN tarefa AS T ON T.nome_cliente = C.nome_cliente AND T.nome_projeto = P.nome_projeto
    WHERE T.ciclo_completo = 'Não'
)
GO
USE [master]
GO
ALTER DATABASE [db_projetos] SET  READ_WRITE 
GO
