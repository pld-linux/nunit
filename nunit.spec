%include	/usr/lib/rpm/macros.mono
Summary:	Unit test framework for CLI
Summary(pl.UTF-8):	Szkielet testów jednostkowych dla CLI
Name:		nunit
Version:	3.9
Release:	1
License:	MIT
Group:		Development/Tools
#Source0Download: https://github.com/nunit/nunit/releases
Source0:	https://github.com/nunit/nunit/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a5692defc73351c5b12c6ddd78c107cd
Source1:	%{name}.pc
Source2:	nunitlite-runner.sh
URL:		http://www.nunit.org/
BuildRequires:	mono-devel >= 4.0
BuildRequires:	rpmbuild(monoautodeps)
Requires:	dotnet-nunit = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 ia64 mips ppc ppc64 s390x sparc sparcv9 sparc64
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NUnit is a unit testing framework for all .NET languages. It serves
the same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.

NUnit targets the CLI (Common Language Infrastructure) and supports
Mono and the Microsoft .NET Framework.

%description -l pl.UTF-8
NUnit to szkielet do testów jednostkowych dla wszystkich języków .NET.
Służy do tego samego celu, co JUnit w świecie Javy. Obsługuje
kategorie testów, testy pod kątem wyjątków oraz zapis wyników testów w
pliku tekstowym lub XML.

NUnit jest przeznaczony dla CLI (Common Language Infrastructure),
obsługuje Mono oraz Microsoft .NET Framework.

%package -n dotnet-nunit
Summary:	NUnit 3.x library for .NET
Summary(pl.UTF-8):	Biblioteka NUnit 3.x dla .NET
Group:		Libraries
Requires:	mono >= 4.0

%description -n dotnet-nunit
NUnit 3.x library for .NET.

%description -n dotnet-nunit -l pl.UTF-8
Biblioteka NUnit 3.x dla .NET.

%package -n dotnet-nunit-devel
Summary:	Development files for NUnit 3.x
Summary(pl.UTF-8):	Pliki programistyczne pakietu NUnit 3.x
Group:		Development/Libraries
Requires:	dotnet-nunit = %{version}-%{release}
Requires:	mono-devel >= 4.0
Obsoletes:	nunit-devel

%description -n dotnet-nunit-devel
Development files for NUnit 3.x.

%description -n dotnet-nunit-devel -l pl.UTF-8
Pliki programistyczne pakietu NUnit 3.x.

%prep
%setup -q

%build
xbuild /property:Configuration=Release src/NUnitFramework/framework/nunit.framework-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/nunitlite/nunitlite-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/nunitlite-runner/nunitlite-runner-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/mock-assembly/mock-assembly-4.5.csproj

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/usr/lib/mono/nunit,%{_pkgconfigdir},%{_bindir}}

gacutil -f -i bin/Release/net-4.5/nunit.framework.dll -package nunit -gacdir $RPM_BUILD_ROOT/usr/lib
gacutil -f -i bin/Release/net-4.5/nunitlite.dll -package nunit -gacdir $RPM_BUILD_ROOT/usr/lib
install bin/Release/net-4.5/*.exe $RPM_BUILD_ROOT/usr/lib/mono/nunit
cp -p bin/Release/net-4.5/nunitlite-runner.exe.config $RPM_BUILD_ROOT/usr/lib/mono/nunit
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_pkgconfigdir}/nunit.pc
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/nunitlite-runner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.txt NOTICES.txt README.md
%attr(755,root,root) %{_bindir}/nunitlite-runner

%files -n dotnet-nunit
%defattr(644,root,root,755)
/usr/lib/mono/gac/nunit.framework
/usr/lib/mono/gac/nunitlite
%dir /usr/lib/mono/nunit
%attr(755,root,root) /usr/lib/mono/nunit/mock-assembly.exe
%attr(755,root,root) /usr/lib/mono/nunit/nunitlite-runner.exe
/usr/lib/mono/nunit/nunitlite-runner.exe.config

%files -n dotnet-nunit-devel
%defattr(644,root,root,755)
/usr/lib/mono/nunit/nunit.framework.dll
/usr/lib/mono/nunit/nunitlite.dll
%{_pkgconfigdir}/nunit.pc
