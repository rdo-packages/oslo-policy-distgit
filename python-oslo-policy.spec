%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.policy
%global pkg_name oslo-policy
%global with_doc 1
%global common_desc \
An OpenStack library for policy.

%global common_desc1 \
Test subpackage for the Oslo policy library.

%if 0%{?fedora} >=24
%global with_python3 1
%endif

Name:           python-%{pkg_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack oslo.policy library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n python2-%{pkg_name}
Summary:        OpenStack oslo.policy library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
# test dependencies
BuildRequires:  python2-hacking
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-context
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-oslotest
BuildRequires:  python2-fixtures
BuildRequires:  python2-mock
BuildRequires:  python2-requests
BuildRequires:  python2-stevedore
BuildRequires:  python2-stestr
BuildRequires:  python2-sphinx
# Required to compile translation files
BuildRequires:  python2-babel
%if 0%{?fedora} > 0
BuildRequires:  python2-requests-mock
BuildRequires:  python2-docutils
BuildRequires:  python2-pyyaml >= 3.1.0
%else
BuildRequires:  python-requests-mock
BuildRequires:  python-docutils
BuildRequires:  PyYAML >= 3.1.0
%endif

Requires:       python2-requests
Requires:       python2-oslo-config >= 2:5.1.0
Requires:       python2-oslo-context >= 2.21.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-six >= 1.10.0
Requires:       python2-stevedore >= 1.20.0
%if 0%{?fedora} > 0
Requires:       python2-pyyaml >= 3.10
%else
Requires:       PyYAML >= 3.10
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo policy library

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-oslo-i18n

%description -n python-%{pkg_name}-doc
Documentation for the Oslo policy library.
%endif

%package -n python2-%{pkg_name}-tests
Summary:    Test subpackage for the Oslo policy library
%{?python_provide:%python_provide python2-%{pkg_name}}

Requires:  python2-%{pkg_name} = %{version}-%{release}
Requires:  python2-hacking
Requires:  python2-oslotest
Requires:  python2-fixtures
Requires:  python2-mock
Requires:  python2-requests
%if 0%{?fedora} > 0
Requires:  python2-requests-mock
%else
Requires:  python-requests-mock
%endif

%description -n python2-%{pkg_name}-tests
%{common_desc1}

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack oslo.policy library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# test dependencies
BuildRequires:  python3-docutils
BuildRequires:  python3-hacking
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-context
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslotest
BuildRequires:  python3-requests-mock
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-requests
BuildRequires:  python3-PyYAML >= 3.1.0
BuildRequires:  python3-sphinx
BuildRequires:  python3-stevedore
BuildRequires:  python3-stestr

Requires:       python3-oslo-config >= 2:5.1.0
Requires:       python3-oslo-context >= 2.21.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-six >= 1.10.0
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-PyYAML >= 3.10
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}
%endif

%if 0%{?with_python3}
%package -n python3-%{pkg_name}-tests
Summary:    Test subpackage for the Oslo policy library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-oslotest
Requires:  python3-requests-mock
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-requests

%description -n python3-%{pkg_name}-tests
%{common_desc1}
%endif

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo policy library

%description -n python-%{pkg_name}-lang
Translation files for Oslo policy library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -f *requirements.txt

# FIXME (jpena): Remove buggy PO-Revision-Date lines in translation
# See https://bugs.launchpad.net/openstack-i18n/+bug/1586041 for details
sed -i '/^\"PO-Revision-Date: \\n\"/d' oslo_policy/locale/*/LC_MESSAGES/*.po

%build
%py2_build

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_policy/locale

%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif

%py2_install

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_policy/locale/*/LC_*/oslo_policy*po
rm -f %{buildroot}%{python2_sitelib}/oslo_policy/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_policy/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_policy/locale
%endif

# Find language files
%find_lang oslo_policy --all-name

%check
export OS_TEST_PATH="./oslo_policy/tests"
%if 0%{?with_python3}
stestr-3 --test-path $OS_TEST_PATH run
%endif
stestr --test-path $OS_TEST_PATH run

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslopolicy-checker
%{_bindir}/oslopolicy-list-redundant
%{_bindir}/oslopolicy-policy-generator
%{_bindir}/oslopolicy-sample-generator
%{python2_sitelib}/oslo_policy
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_policy/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_policy/tests

%files -n python-%{pkg_name}-lang -f oslo_policy.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_policy
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_policy/tests
%endif

%if 0%{?with_python3}
%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_policy/tests
%endif

%changelog
